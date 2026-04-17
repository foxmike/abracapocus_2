from pathlib import Path

from config import load_config
from models.plan import Plan, PlanPhase, PlanTask
from models.project import TaskDocument
from models.reports import BackendExecution, ReviewReport, VerificationReport
from orchestrator.supervisor import PhaseResult, SupervisorOrchestrator, TaskResult


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


def _phase_result(changed_files):
    task = TaskDocument(task_id="t1", title="Task", description="desc", phase="implementation")
    execution = BackendExecution(
        backend="codex_cli",
        command=["cmd"],
        stdout="",
        stderr="",
        exit_code=0,
        duration_seconds=0.1,
        changed_files=changed_files,
        diff_summary="",
    )
    task_result = TaskResult(
        task=task,
        execution=execution,
        review=ReviewReport(status="approved", findings=[], summary="ok"),
        status="passed",
    )
    verification = VerificationReport(status="passed", checks=[], notes="", profile="strict")
    return PhaseResult(
        phase_name="Implementation",
        task_results=[task_result],
        verification=verification,
        status="passed",
    )


def test_successful_phase_with_changes_commits(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    orchestrator = SupervisorOrchestrator(config)
    captured = {}
    monkeypatch.setattr(orchestrator.git_manager, "commit_changes", lambda message: captured.setdefault("message", message) or True)

    plan = Plan(
        project_name="p",
        summary="s",
        phases=[
            PlanPhase(
                name="Implementation",
                objective="obj",
                tasks=[PlanTask(task=TaskDocument(task_id="t1", title="Task", description="desc", phase="implementation"))],
            )
        ],
        version="v1",
    )
    state = {
        "plan": plan,
        "phase_index": 0,
        "phase_results": [_phase_result([{"path": "a.py"}])],
        "run_id": "12345678-aaaa",
    }

    orchestrator._phase_advance(state)

    assert captured["message"] == "abracapocus: phase Implementation complete [12345678]"


def test_empty_phase_changes_skips_commit(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    orchestrator = SupervisorOrchestrator(config)
    called = {"value": False}
    monkeypatch.setattr(orchestrator.git_manager, "commit_changes", lambda message: called.__setitem__("value", True) or True)

    plan = Plan(
        project_name="p",
        summary="s",
        phases=[
            PlanPhase(
                name="Implementation",
                objective="obj",
                tasks=[PlanTask(task=TaskDocument(task_id="t1", title="Task", description="desc", phase="implementation"))],
            )
        ],
        version="v1",
    )
    state = {
        "plan": plan,
        "phase_index": 0,
        "phase_results": [_phase_result([])],
        "run_id": "12345678-aaaa",
    }

    orchestrator._phase_advance(state)

    assert called["value"] is False

