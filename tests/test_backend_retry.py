from pathlib import Path
from types import SimpleNamespace
import subprocess

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class DummyBackend(CodingBackend):
    name = "dummy"
    executable = "dummy"

    def __init__(self, tmp_path: Path, max_retries: int = 3, retry_delay_base: float = 2.0):
        super().__init__(
            prompt_path=Path("prompts/demo_cli.md"),
            working_root=tmp_path,
            timeout=1,
            max_retries=max_retries,
            retry_delay_base=retry_delay_base,
        )
        self.supports_direct_execution = True

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None):
        return ["dummy", task.task_id]

    def _can_run_cli(self) -> bool:
        return True


def _task() -> TaskDocument:
    return TaskDocument(task_id="t", title="T", description="D", phase="p")


def _context() -> ContextPackage:
    return ContextPackage(summaries=[], files=[], notes="")


def test_rate_limit_stderr_triggers_retry_with_backoff(monkeypatch, tmp_path):
    backend = DummyBackend(tmp_path, max_retries=2, retry_delay_base=2.0)
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    responses = [
        SimpleNamespace(stdout="", stderr="Rate limit exceeded", returncode=1),
        SimpleNamespace(stdout="ok", stderr="", returncode=0),
    ]
    sleeps = []

    monkeypatch.setattr("random.random", lambda: 0.5)
    monkeypatch.setattr("time.sleep", lambda value: sleeps.append(value))
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: responses.pop(0))

    result = backend.execute(_task(), _context(), dry_run=False)

    assert result.exit_code == 0
    assert sleeps == [2.5]


def test_timeout_expired_retries_up_to_max_retries(monkeypatch, tmp_path):
    backend = DummyBackend(tmp_path, max_retries=2, retry_delay_base=1.0)
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    calls = {"count": 0}
    sleeps = []

    def fake_run(*args, **kwargs):
        calls["count"] += 1
        raise subprocess.TimeoutExpired(cmd="dummy", timeout=1)

    monkeypatch.setattr("random.random", lambda: 0.0)
    monkeypatch.setattr("time.sleep", lambda value: sleeps.append(value))
    monkeypatch.setattr("subprocess.run", fake_run)

    result = backend.execute(_task(), _context(), dry_run=False)

    assert result.exit_code == 1
    assert calls["count"] == 3
    assert sleeps == [1.0, 2.0]


def test_bad_args_exit_code_two_fails_without_retry(monkeypatch, tmp_path):
    backend = DummyBackend(tmp_path, max_retries=3, retry_delay_base=1.0)
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    calls = {"count": 0}

    def fake_run(*args, **kwargs):
        calls["count"] += 1
        return SimpleNamespace(stdout="", stderr="bad args", returncode=2)

    monkeypatch.setattr("subprocess.run", fake_run)

    result = backend.execute(_task(), _context(), dry_run=False)

    assert result.exit_code == 2
    assert calls["count"] == 1


def test_retry_count_logged_per_execution(monkeypatch, tmp_path, caplog):
    backend = DummyBackend(tmp_path, max_retries=1, retry_delay_base=1.0)
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    responses = [
        SimpleNamespace(stdout="", stderr="429 rate limit", returncode=1),
        SimpleNamespace(stdout="ok", stderr="", returncode=0),
    ]
    monkeypatch.setattr("random.random", lambda: 0.0)
    monkeypatch.setattr("time.sleep", lambda _value: None)
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: responses.pop(0))

    with caplog.at_level("INFO"):
        backend.execute(_task(), _context(), dry_run=False)

    assert any("retry_count=1" in message for message in caplog.messages)
