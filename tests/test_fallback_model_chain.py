from pathlib import Path
from types import SimpleNamespace

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class DummyFallbackBackend(CodingBackend):
    name = "dummy_fallback"
    executable = "dummy"

    def __init__(self, tmp_path: Path):
        super().__init__(prompt_path=Path("prompts/demo_cli.md"), working_root=tmp_path)
        self.supports_direct_execution = True

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None):
        return ["dummy", model or "default"]

    def _can_run_cli(self) -> bool:
        return True


def _task() -> TaskDocument:
    return TaskDocument(task_id="t", title="T", description="D", phase="p")


def _context() -> ContextPackage:
    return ContextPackage(summaries=[], files=[], notes="")


def test_two_model_list_tries_second_on_first_failure(monkeypatch, tmp_path):
    backend = DummyFallbackBackend(tmp_path)
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    responses = [
        SimpleNamespace(stdout="", stderr="hard fail", returncode=2),
        SimpleNamespace(stdout="ok", stderr="", returncode=0),
    ]
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: responses.pop(0))

    result = backend.execute(_task(), _context(), dry_run=False, model=["m1", "m2"])

    assert result.exit_code == 0
    assert result.model_attempts == ["m1", "m2"]
    assert result.model == "m2"


def test_all_models_exhausted_returns_failure_with_attempt_log(monkeypatch, tmp_path):
    backend = DummyFallbackBackend(tmp_path)
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    responses = [
        SimpleNamespace(stdout="", stderr="bad args", returncode=2),
        SimpleNamespace(stdout="", stderr="bad args", returncode=2),
    ]
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: responses.pop(0))

    result = backend.execute(_task(), _context(), dry_run=False, model=["m1", "m2"])

    assert result.exit_code != 0
    assert result.model_attempts == ["m1", "m2"]
    assert result.model == "m2"

