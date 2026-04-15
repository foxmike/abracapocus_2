from pathlib import Path

from backends.codex_cli import CodexCliBackend
from models.project import ContextPackage, TaskDocument


class DummyProcess:
    def __init__(self, stdout: str = "", stderr: str = "", returncode: int = 0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


def _sample_task() -> TaskDocument:
    return TaskDocument(
        task_id="task-42",
        title="Implement feature",
        description="Do something real",
        phase="implementation",
    )


def _sample_context() -> ContextPackage:
    return ContextPackage(summaries=["s"], files=["main.py"], notes="context")


def _sample_context_with_agents() -> ContextPackage:
    return ContextPackage(
        summaries=["s"],
        files=["main.py"],
        notes="context",
        agents_md="# AGENTS\n- rule one",
        agents_metadata={"loaded": True},
    )


def test_codex_backend_executes_cli(monkeypatch, tmp_path):
    backend = CodexCliBackend(working_root=tmp_path)
    backend.workdir = Path(tmp_path)
    recorded = {}
    monkeypatch.setattr(CodexCliBackend, "_can_run_cli", lambda self: True)
    snapshots = iter(
        [
            ({"main.py": " M"}, None),
            ({"main.py": " M", "README.md": "??"}, None),
        ]
    )

    def fake_status(self, workdir):
        return next(snapshots)

    monkeypatch.setattr(CodexCliBackend, "_git_status_snapshot", fake_status)
    monkeypatch.setattr(CodexCliBackend, "_git_diff_summary", lambda self, workdir, paths: "diff summary")

    def fake_run(command, capture_output, text, timeout, check, cwd):
        recorded["command"] = command
        recorded["cwd"] = cwd
        recorded["timeout"] = timeout
        return DummyProcess(stdout="ok", stderr="")

    monkeypatch.setattr("subprocess.run", fake_run)
    task = _sample_task()
    context = _sample_context()
    result = backend.execute(task, context, dry_run=False)

    assert recorded["cwd"] == str(tmp_path)
    assert recorded["command"][0] == "codex"
    assert recorded["command"][1] == "exec"
    assert "--full-auto" in recorded["command"]
    assert "-m" in recorded["command"]
    model_index = recorded["command"].index("-m")
    assert recorded["command"][model_index + 1] == "gpt-5.3-codex"
    assert "-C" in recorded["command"]
    cd_index = recorded["command"].index("-C")
    assert recorded["command"][cd_index + 1] == str(tmp_path)
    assert any("Implement feature" in arg for arg in recorded["command"])
    assert result.stdout == "ok"
    assert result.exit_code == 0
    assert result.working_directory == str(tmp_path)
    assert result.changed_files
    assert result.diff_summary == "diff summary"


def test_codex_backend_handles_cli_errors(monkeypatch, tmp_path):
    backend = CodexCliBackend(working_root=tmp_path)
    backend.workdir = Path(tmp_path)
    monkeypatch.setattr(CodexCliBackend, "_can_run_cli", lambda self: True)
    monkeypatch.setattr(CodexCliBackend, "_git_status_snapshot", lambda self, workdir: ({}, None))
    monkeypatch.setattr(CodexCliBackend, "_git_diff_summary", lambda self, workdir, paths: "")

    def fake_run(command, capture_output, text, timeout, check, cwd):
        return DummyProcess(stdout="", stderr="boom", returncode=12)

    monkeypatch.setattr("subprocess.run", fake_run)
    task = _sample_task()
    context = _sample_context()
    result = backend.execute(task, context, dry_run=False)

    assert result.exit_code == 12
    assert "boom" in result.stderr
    assert result.working_directory == str(tmp_path)
    assert result.diff_summary in {"", "No file changes detected"}


def test_codex_backend_git_unavailable(monkeypatch, tmp_path):
    backend = CodexCliBackend(working_root=tmp_path)
    backend.workdir = Path(tmp_path)
    monkeypatch.setattr(CodexCliBackend, "_can_run_cli", lambda self: False)
    monkeypatch.setattr(
        CodexCliBackend,
        "_git_status_snapshot",
        lambda self, workdir: (None, "git missing"),
    )
    task = _sample_task()
    context = _sample_context()
    result = backend.execute(task, context, dry_run=False)
    assert result.changed_files == []
    assert "git metadata unavailable" in result.diff_summary


def test_codex_backend_includes_agents_md_prompt():
    backend = CodexCliBackend(working_root=Path.cwd())
    command = backend.build_command(_sample_task(), _sample_context_with_agents())
    assert any("AGENTS.md" in token for token in command)
    assert any("rule one" in token for token in command)
    assert any("AGENTS metadata" in token for token in command)
    assert any('"loaded": true' in token for token in command)


def test_codex_backend_includes_acceptance_criteria_in_prompt():
    backend = CodexCliBackend(working_root=Path.cwd())
    task = TaskDocument(
        task_id="task-acceptance",
        title="Implement feature",
        description="Do something real",
        phase="implementation",
        acceptance_criteria=["criterion one", "criterion two"],
    )
    command = backend.build_command(task, _sample_context())
    assert any("Acceptance criteria:" in token for token in command)
    assert any("criterion one" in token for token in command)
    assert any("criterion two" in token for token in command)


def test_codex_backend_respects_env_model_override(monkeypatch):
    monkeypatch.setenv("CODEX_MODEL", "custom-codex-model")
    backend = CodexCliBackend(working_root=Path.cwd())
    command = backend.build_command(_sample_task(), _sample_context())
    assert "-m" in command
    idx = command.index("-m")
    assert command[idx + 1] == "custom-codex-model"
