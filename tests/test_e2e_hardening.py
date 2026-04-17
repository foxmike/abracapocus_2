from pathlib import Path
from types import SimpleNamespace

from backends.base import CodingBackend
from config import load_config
from models.project import ContextPackage, ProjectRequest, TaskDocument
from models.reports import (
    BackendExecution,
    ChangeAssessment,
    OrchestrationReport,
    ReviewReport,
    VerificationCheck,
    VerificationReport,
)
from orchestrator.supervisor import SupervisorOrchestrator
from runtime.failure_classifier import FailureClassification


class DummyHardeningBackend(CodingBackend):
    name = "codex_cli"
    executable = "dummy"

    def __init__(self, tmp_path: Path):
        super().__init__(prompt_path=Path("prompts/demo_cli.md"), working_root=tmp_path)
        self.supports_direct_execution = True

    def build_command(self, task: TaskDocument, context: ContextPackage, model=None):
        return ["dummy", task.task_id, model or "default"]

    def _can_run_cli(self) -> bool:
        return True


def _task() -> TaskDocument:
    return TaskDocument(task_id="t", title="T", description="D", phase="implementation")


def _context() -> ContextPackage:
    return ContextPackage(summaries=[], files=[], notes="")


def _tmp_config(tmp_path: Path):
    config = load_config()
    paths = config.paths.model_copy(
        update={
            "working_root": tmp_path,
            "root_dir": tmp_path,
            "logs_dir": tmp_path / "logs",
            "reports_dir": tmp_path / "reports",
            "plans_dir": tmp_path / "plans",
            "tasks_dir": tmp_path / "tasks",
            "phases_dir": tmp_path / "phases",
            "state_file": tmp_path / "state" / "runtime_state.json",
        }
    )
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    paths.reports_dir.mkdir(parents=True, exist_ok=True)
    paths.plans_dir.mkdir(parents=True, exist_ok=True)
    paths.tasks_dir.mkdir(parents=True, exist_ok=True)
    paths.phases_dir.mkdir(parents=True, exist_ok=True)
    paths.state_file.parent.mkdir(parents=True, exist_ok=True)
    config.paths = paths
    return config


def test_retry_behavior_on_rate_limit(monkeypatch, tmp_path):
    backend = DummyHardeningBackend(tmp_path)
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    responses = [
        SimpleNamespace(stdout="", stderr="429 rate limit", returncode=1),
        SimpleNamespace(stdout="ok", stderr="", returncode=0),
    ]
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: responses.pop(0))
    monkeypatch.setattr("random.random", lambda: 0.0)
    monkeypatch.setattr("time.sleep", lambda _seconds: None)

    result = backend.execute(_task(), _context(), dry_run=False)

    assert result.exit_code == 0


def test_fallback_chain_records_model_attempts(monkeypatch, tmp_path):
    backend = DummyHardeningBackend(tmp_path)
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    responses = [
        SimpleNamespace(stdout="", stderr="bad args", returncode=2),
        SimpleNamespace(stdout="ok", stderr="", returncode=0),
    ]
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: responses.pop(0))

    result = backend.execute(_task(), _context(), dry_run=False, model=["m1", "m2"])

    assert result.model_attempts == ["m1", "m2"]
    assert result.model == "m2"


def test_pace_control_blocks_with_sleep(monkeypatch, tmp_path):
    backend = DummyHardeningBackend(tmp_path)
    backend.min_seconds_between_calls = 5.0
    backend.max_calls_per_minute = 0
    monkeypatch.setattr(backend, "_git_status_snapshot", lambda workdir: ({}, None))
    monkeypatch.setattr(backend, "_collect_repo_deltas", lambda workdir, before_snapshot, before_error: ([], ""))
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: SimpleNamespace(stdout="ok", stderr="", returncode=0))
    now = {"value": 100.0}
    sleeps = []
    monkeypatch.setattr("time.time", lambda: now["value"])
    monkeypatch.setattr("time.sleep", lambda seconds: (sleeps.append(seconds), now.__setitem__("value", now["value"] + seconds)))

    backend.execute(_task(), _context(), dry_run=False)
    backend.execute(_task(), _context(), dry_run=False)

    assert sleeps and round(sleeps[0], 2) == 5.0


def test_branch_creation_called_before_run(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    orchestrator = SupervisorOrchestrator(config)
    captured = {"branch": ""}
    monkeypatch.setattr(orchestrator.git_manager, "safe_to_run", lambda: True)
    monkeypatch.setattr(orchestrator.git_manager, "create_branch", lambda name: captured.__setitem__("branch", name) or True)

    def fake_run_without_langgraph(_initial_state):
        return OrchestrationReport(
            plan_summary="summary",
            backend_executions=[],
            review=ReviewReport(status="approved", findings=[], summary="ok"),
            verification=VerificationReport(status="passed", checks=[], notes="", profile="strict"),
            change_assessment=ChangeAssessment(
                task_intent="intent",
                changed_files_summary="none",
                verification_summary="passed",
                assessment_status="aligned",
            ),
            metadata={"run_id": "rid", "branch_name": captured["branch"]},
        )

    monkeypatch.setattr(orchestrator, "_run_without_langgraph", fake_run_without_langgraph)

    report = orchestrator.run(ProjectRequest(project_name="p", goal="g", context="c"), task=_task())

    assert captured["branch"].startswith("abracapocus/t-")
    assert report.metadata["branch_name"].startswith("abracapocus/t-")


def test_blocked_task_persistence_writes_report(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    orchestrator = SupervisorOrchestrator(config)
    task = _task()
    verification = VerificationReport(
        status="failed",
        checks=[VerificationCheck(name="pytest", status="failed", detail="boom")],
        notes="failed",
        profile="strict",
    )
    attempts = [
        BackendExecution(
            backend="codex_cli",
            command=["cmd"],
            stdout="",
            stderr="boom",
            exit_code=1,
            duration_seconds=0.1,
        )
    ]
    classification = FailureClassification(
        failure_type="unknown",
        affected_files=[],
        failure_detail="boom",
        retry_likely=False,
        suggested_focus="investigate",
    )

    blocked_path = orchestrator._persist_blocked_report(task, "runid", attempts, verification, classification)

    assert Path(blocked_path).exists()

