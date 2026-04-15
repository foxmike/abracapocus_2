from pathlib import Path

import pytest

from backends.aider_cli import AiderCliBackend
from backends.base import CodingBackend, SecurityError
from backends.codex_cli import CodexCliBackend
from config import load_config
from models.project import ContextPackage, TaskDocument


class DummyBackend(CodingBackend):
    name = "dummy"
    executable = "dummy"


def _sample_task() -> TaskDocument:
    return TaskDocument(
        task_id="task-sandbox",
        title="Sandbox",
        description="Validate workdir safety",
        phase="phase_0",
    )


def _sample_context() -> ContextPackage:
    return ContextPackage(summaries=["s"], files=["main.py"], notes="context")


def test_execute_allows_workdir_equal_working_root(monkeypatch, tmp_path):
    backend = DummyBackend(prompt_path=Path("prompts/demo_cli.md"), working_root=tmp_path)
    backend.workdir = tmp_path

    monkeypatch.setattr(DummyBackend, "_git_status_snapshot", lambda self, workdir: ({}, None))
    monkeypatch.setattr(DummyBackend, "_collect_repo_deltas", lambda self, workdir, before_snapshot, before_error: ([], ""))

    result = backend.execute(_sample_task(), _sample_context(), dry_run=True)

    assert result.exit_code == 0


def test_execute_allows_workdir_inside_working_root(monkeypatch, tmp_path):
    backend = DummyBackend(prompt_path=Path("prompts/demo_cli.md"), working_root=tmp_path)
    nested = tmp_path / "nested"
    nested.mkdir()
    backend.workdir = nested

    monkeypatch.setattr(DummyBackend, "_git_status_snapshot", lambda self, workdir: ({}, None))
    monkeypatch.setattr(DummyBackend, "_collect_repo_deltas", lambda self, workdir, before_snapshot, before_error: ([], ""))

    result = backend.execute(_sample_task(), _sample_context(), dry_run=True)

    assert result.exit_code == 0


def test_execute_blocks_workdir_outside_working_root_before_subprocess(monkeypatch, tmp_path):
    backend = DummyBackend(prompt_path=Path("prompts/demo_cli.md"), working_root=tmp_path)
    backend.workdir = tmp_path.parent

    def fail_if_git_status_called(self, workdir):
        raise AssertionError("git status path reached before safety guard")

    def fail_if_subprocess_called(*args, **kwargs):
        raise AssertionError("subprocess path reached before safety guard")

    monkeypatch.setattr(DummyBackend, "_git_status_snapshot", fail_if_git_status_called)
    monkeypatch.setattr(DummyBackend, "_can_run_cli", lambda self: True)
    monkeypatch.setattr("subprocess.run", fail_if_subprocess_called)

    with pytest.raises(SecurityError) as exc:
        backend.execute(_sample_task(), _sample_context(), dry_run=False)

    message = str(exc.value)
    assert str(backend.workdir.resolve()) in message
    assert str(backend.working_root.resolve()) in message


def test_aider_command_includes_root_flag(tmp_path):
    backend = AiderCliBackend(working_root=tmp_path)
    command = backend.build_command(_sample_task(), _sample_context())

    assert "--root" in command
    root_index = command.index("--root")
    assert command[root_index + 1] == str(backend.workdir)


def test_codex_command_includes_c_flag(tmp_path):
    backend = CodexCliBackend(working_root=tmp_path)
    command = backend.build_command(_sample_task(), _sample_context())

    assert "-C" in command
    workdir_index = command.index("-C")
    assert command[workdir_index + 1] == str(backend.workdir)


def test_working_root_loads_from_env(monkeypatch, tmp_path):
    monkeypatch.setenv("ABRACAPOCUS_WORKING_ROOT", str(tmp_path))

    config = load_config()

    assert config.paths.working_root == tmp_path
