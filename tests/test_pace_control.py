from pathlib import Path
from types import SimpleNamespace

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class DummyPaceBackend(CodingBackend):
    name = "aider_cli"
    executable = "dummy"

    def __init__(self, tmp_path: Path):
        super().__init__(prompt_path=Path("prompts/demo_cli.md"), working_root=tmp_path)
        self.supports_direct_execution = True

    def build_command(self, task: TaskDocument, context: ContextPackage, model=None):
        return ["dummy", task.task_id]

    def _can_run_cli(self) -> bool:
        return True


def _task() -> TaskDocument:
    return TaskDocument(task_id="t", title="T", description="D", phase="p")


def _context() -> ContextPackage:
    return ContextPackage(summaries=[], files=[], notes="")


def test_aider_min_delay_enforced_from_env(monkeypatch, tmp_path):
    monkeypatch.setenv("AIDER_MIN_DELAY", "5")
    backend = DummyPaceBackend(tmp_path)
    backend.max_calls_per_minute = 0
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: SimpleNamespace(stdout="ok", stderr="", returncode=0))

    now = {"value": 100.0}
    sleeps = []
    monkeypatch.setattr("time.time", lambda: now["value"])

    def fake_sleep(seconds: float):
        sleeps.append(seconds)
        now["value"] += seconds

    monkeypatch.setattr("time.sleep", fake_sleep)

    backend.execute(_task(), _context(), dry_run=False)
    backend.execute(_task(), _context(), dry_run=False)

    assert sleeps == [5.0]


def test_pace_delay_logged_at_info(monkeypatch, tmp_path, caplog):
    monkeypatch.setenv("AIDER_MIN_DELAY", "2")
    backend = DummyPaceBackend(tmp_path)
    backend.max_calls_per_minute = 0
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: SimpleNamespace(stdout="ok", stderr="", returncode=0))

    now = {"value": 50.0}
    monkeypatch.setattr("time.time", lambda: now["value"])
    monkeypatch.setattr("time.sleep", lambda seconds: now.__setitem__("value", now["value"] + seconds))

    with caplog.at_level("INFO"):
        backend.execute(_task(), _context(), dry_run=False)
        backend.execute(_task(), _context(), dry_run=False)

    assert any("pace_delay_seconds" in message for message in caplog.messages)


def test_max_calls_per_minute_enforced_with_sleep(monkeypatch, tmp_path):
    monkeypatch.setenv("AIDER_MIN_DELAY", "0")
    backend = DummyPaceBackend(tmp_path)
    backend.max_calls_per_minute = 2
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: SimpleNamespace(stdout="ok", stderr="", returncode=0))

    now = {"value": 100.0}
    sleeps = []
    monkeypatch.setattr("time.time", lambda: now["value"])

    def fake_sleep(seconds: float):
        sleeps.append(seconds)
        now["value"] += seconds

    monkeypatch.setattr("time.sleep", fake_sleep)

    backend.execute(_task(), _context(), dry_run=False)
    backend.execute(_task(), _context(), dry_run=False)
    backend.execute(_task(), _context(), dry_run=False)

    assert sleeps
    assert round(sleeps[0], 2) == 60.0

