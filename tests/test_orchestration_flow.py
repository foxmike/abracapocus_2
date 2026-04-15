from pathlib import Path

from config import load_config
from models.project import ProjectRequest, TaskDocument
from models.reports import BackendExecution, VerificationReport
from orchestrator.supervisor import SupervisorOrchestrator, run_demo
from runtime.state_store import StateStore


def test_demo_flow_runs(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    report = run_demo()
    assert report.backend_executions
    assert report.backend_execution.exit_code == 0
    assert report.review.status in {"approved", "changes_requested"}
    assert report.verification.status in {"passed", "failed"}
    assert report.metadata.get("task_id")
    assert report.metadata.get("selected_backend")


def test_run_with_task_document(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = load_config()
    orchestrator = SupervisorOrchestrator(config)
    task = TaskDocument(
        task_id="custom-task",
        title="Custom Work",
        description="Execute custom task",
        phase="implementation",
        selected_backend="aider_cli",
        verification_profile="minimal",
    )
    request = ProjectRequest(project_name=config.project_name, goal=task.description, context="manual-run")
    report = orchestrator.run(request, task=task)
    assert report.metadata["task_id"] == "custom-task"
    assert report.metadata["selected_backend"] == "aider_cli"
    assert report.metadata["verification_profile"] == "minimal"


def test_runtime_backend_override(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    store = StateStore(config)
    store.reset()

    def _set_override(state):
        state.operator_overrides = {"backend": "gemini_cli"}
        return state

    store.update(_set_override)
    orchestrator = SupervisorOrchestrator(config)
    task = TaskDocument(task_id="t1", title="Override", description="test", phase="build")
    decision = orchestrator.router.select(task)
    assert decision.backend_name == "gemini_cli"


def test_routing_decision_backend_uses_config_working_root(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    orchestrator = SupervisorOrchestrator(config)
    task = TaskDocument(task_id="t-root", title="Root", description="root", phase="build")
    decision = orchestrator.router.select(task)

    backend = decision.backend(orchestrator.config.paths.working_root)

    assert backend.working_root == tmp_path


def test_runtime_verification_override(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    store = StateStore(config)
    store.reset()
    store.update(lambda state: state.model_copy(update={"operator_overrides": {"verification_profile": "strict"}}))
    orchestrator = SupervisorOrchestrator(config)
    assert orchestrator.config.verification.active_profile == "strict"


def test_agent_overrides_disable(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    store = StateStore(config)
    store.reset()

    def _set(state):
        state.operator_overrides = {"agents": {"reviewer": False, "verifier": False}}
        return state

    store.update(_set)
    orchestrator = SupervisorOrchestrator(config)
    task = TaskDocument(task_id="no-review", title="Skip", description="skip", phase="impl")
    request = ProjectRequest(project_name=config.project_name, goal="Skip", context="override")
    report = orchestrator.run(request, task=task)
    assert report.review.status == "skipped"
    assert report.verification.status == "skipped"


def test_assessment_aligned(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    orchestrator = SupervisorOrchestrator(config)
    execution = BackendExecution(
        backend="codex_cli",
        command=["cmd"],
        stdout="",
        stderr="",
        exit_code=0,
        duration_seconds=0.1,
        changed_files=[{"path": "file.py", "status": "modified", "code": "M"}],
        diff_summary="file.py | 1 +",
    )
    verification = VerificationReport(status="passed", checks=[], notes="", profile="default")
    assessment = orchestrator._assess_changes(
        TaskDocument(task_id="t", title="demo", description="demo task", phase="impl"),
        [execution],
        verification,
    )
    assert assessment.assessment_status == "aligned"
    assert "file.py" in assessment.changed_files_summary


def test_assessment_not_aligned(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    orchestrator = SupervisorOrchestrator(config)
    execution = BackendExecution(
        backend="codex_cli",
        command=["cmd"],
        stdout="",
        stderr="",
        exit_code=1,
        duration_seconds=0.1,
        changed_files=[],
        diff_summary="",
    )
    verification = VerificationReport(status="failed", checks=[], notes="", profile="default")
    assessment = orchestrator._assess_changes(
        TaskDocument(task_id="t", title="demo", description="demo task", phase="impl"),
        [execution],
        verification,
    )
    assert assessment.assessment_status == "not_aligned"


def _tmp_config(tmp_path: Path):
    config = load_config()
    paths = config.paths.model_copy(
        update={
            "working_root": tmp_path,
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
