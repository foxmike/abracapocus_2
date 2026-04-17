from pathlib import Path

from config import load_config
from models.project import TaskDocument
from models.reports import BackendExecution, ReviewReport, VerificationCheck, VerificationReport
from orchestrator.supervisor import SupervisorOrchestrator, TaskResult


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


def _task_result() -> TaskResult:
    task = TaskDocument(
        task_id="retry-task",
        title="Retry task",
        description="Implement feature behavior",
        phase="implementation",
        acceptance_criteria=["criterion"],
        selected_backend="codex_cli",
        verification_profile="strict",
    )
    execution = BackendExecution(
        backend="codex_cli",
        command=["codex", "exec"],
        stdout="",
        stderr="SyntaxError: invalid syntax",
        exit_code=1,
        duration_seconds=0.2,
        changed_files=[{"path": "app.py", "status": "modified", "code": "M"}],
        diff_summary="app.py | 3 ++-",
    )
    review = ReviewReport(status="changes_requested", findings=[], summary="failed")
    return TaskResult(task=task, execution=execution, review=review, status="failed")


def _verification_failed() -> VerificationReport:
    return VerificationReport(
        status="failed",
        checks=[
            VerificationCheck(
                name="pytest",
                status="failed",
                detail="SyntaxError: invalid syntax",
            )
        ],
        notes="failed",
        profile="strict",
    )


def _verification_passed() -> VerificationReport:
    return VerificationReport(
        status="passed",
        checks=[VerificationCheck(name="pytest", status="passed", detail="ok")],
        notes="passed",
        profile="strict",
    )


def _verification_task() -> TaskDocument:
    return TaskDocument(
        task_id="verify",
        title="Verify",
        description="Verify",
        phase="implementation",
        verification_profile="strict",
    )


def test_syntax_error_triggers_retry_with_enriched_prompt(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    orchestrator = SupervisorOrchestrator(_tmp_config(tmp_path))
    orchestrator.config.retry.max_retries_tier_1 = 1
    orchestrator.config.retry.max_retries_tier_2 = 0
    orchestrator.config.retry.max_retries_tier_3 = 0

    captured = {}

    def fake_execute(task, context, phase_name, forced_model=None):
        captured["description"] = task.description
        return BackendExecution(
            backend="codex_cli",
            command=["codex", "exec"],
            stdout="fixed",
            stderr="",
            exit_code=0,
            duration_seconds=0.2,
            changed_files=[],
            diff_summary="",
        )

    monkeypatch.setattr(orchestrator, "_execute_task_attempt", fake_execute)
    monkeypatch.setattr(orchestrator, "_run_review", lambda task, executions: ReviewReport(status="approved", findings=[], summary="ok"))
    monkeypatch.setattr(orchestrator, "_run_verification", lambda task, executions: _verification_passed())
    monkeypatch.setattr(orchestrator.research_agent, "update_files", lambda changed_files: None)

    results, verification = orchestrator._run_tiered_retry_loop(
        task_results=[_task_result()],
        verification_task=_verification_task(),
        verification=_verification_failed(),
        context=None,
        phase_name="Implementation Phase",
        run_id="run-1",
    )

    assert verification.status == "passed"
    assert results[0].status == "passed"
    assert "Failure detail: SyntaxError: invalid syntax" in captured["description"]
    assert "Do not repeat the same approach used in prior attempt(s)." in captured["description"]


def test_tier_two_uses_stronger_model_after_tier_one_exhaustion(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    orchestrator = SupervisorOrchestrator(_tmp_config(tmp_path))
    orchestrator.config.retry.max_retries_tier_1 = 1
    orchestrator.config.retry.max_retries_tier_2 = 1
    orchestrator.config.retry.max_retries_tier_3 = 0

    verification_sequence = [_verification_failed(), _verification_passed()]
    forced_models = []

    def fake_execute(task, context, phase_name, forced_model=None):
        forced_models.append(forced_model)
        exit_code = 1 if len(forced_models) == 1 else 0
        return BackendExecution(
            backend="codex_cli",
            command=["codex", "exec"],
            stdout="retry",
            stderr="retry",
            exit_code=exit_code,
            duration_seconds=0.2,
            changed_files=[],
            diff_summary="",
            model=forced_model,
        )

    monkeypatch.setattr(orchestrator, "_execute_task_attempt", fake_execute)
    monkeypatch.setattr(orchestrator, "_run_review", lambda task, executions: ReviewReport(status="approved", findings=[], summary="ok"))
    monkeypatch.setattr(orchestrator, "_run_verification", lambda task, executions: verification_sequence.pop(0))
    monkeypatch.setattr(orchestrator, "_select_tier2_model", lambda task, latest_attempt: "stronger-model")
    monkeypatch.setattr(orchestrator.research_agent, "update_files", lambda changed_files: None)

    results, verification = orchestrator._run_tiered_retry_loop(
        task_results=[_task_result()],
        verification_task=_verification_task(),
        verification=_verification_failed(),
        context=None,
        phase_name="Implementation Phase",
        run_id="run-2",
    )

    assert verification.status == "passed"
    assert results[0].status == "passed"
    assert forced_models == [None, "stronger-model"]


def test_all_tiers_exhausted_writes_blocked_report(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    orchestrator = SupervisorOrchestrator(config)
    orchestrator.config.retry.max_retries_tier_1 = 1
    orchestrator.config.retry.max_retries_tier_2 = 1
    orchestrator.config.retry.max_retries_tier_3 = 1

    monkeypatch.setattr(
        orchestrator,
        "_execute_task_attempt",
        lambda task, context, phase_name, forced_model=None: BackendExecution(
            backend="codex_cli",
            command=["codex", "exec"],
            stdout="retry",
            stderr="retry",
            exit_code=1,
            duration_seconds=0.2,
            changed_files=[],
            diff_summary="",
        ),
    )
    monkeypatch.setattr(orchestrator, "_run_review", lambda task, executions: ReviewReport(status="changes_requested", findings=[], summary="retry"))
    monkeypatch.setattr(orchestrator, "_run_verification", lambda task, executions: _verification_failed())
    monkeypatch.setattr(orchestrator.research_agent, "update_files", lambda changed_files: None)

    results, verification = orchestrator._run_tiered_retry_loop(
        task_results=[_task_result()],
        verification_task=_verification_task(),
        verification=_verification_failed(),
        context=None,
        phase_name="Implementation Phase",
        run_id="blocked-run",
    )

    blocked_path = config.paths.reports_dir / "blocked-retry-task-blocked-run.json"
    assert results[0].status == "blocked"
    assert blocked_path.exists()
    assert "blocked_report=" in verification.notes


def test_passing_verification_exits_without_retry(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    orchestrator = SupervisorOrchestrator(_tmp_config(tmp_path))

    monkeypatch.setattr(
        orchestrator,
        "_execute_task_attempt",
        lambda task, context, phase_name, forced_model=None: (_ for _ in ()).throw(
            AssertionError("retry execution should not be called")
        ),
    )

    results, verification = orchestrator._run_tiered_retry_loop(
        task_results=[_task_result()],
        verification_task=_verification_task(),
        verification=_verification_passed(),
        context=None,
        phase_name="Implementation Phase",
        run_id="run-4",
    )

    assert verification.status == "passed"
    assert results[0].status == "failed"


def test_loop_is_bounded_by_total_retry_limit(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    orchestrator = SupervisorOrchestrator(config)
    orchestrator.config.retry.max_retries_tier_1 = 1
    orchestrator.config.retry.max_retries_tier_2 = 1
    orchestrator.config.retry.max_retries_tier_3 = 1

    attempts = {"count": 0}

    def fake_execute(task, context, phase_name, forced_model=None):
        attempts["count"] += 1
        return BackendExecution(
            backend="codex_cli",
            command=["codex", "exec"],
            stdout="retry",
            stderr="retry",
            exit_code=1,
            duration_seconds=0.2,
            changed_files=[],
            diff_summary="",
        )

    monkeypatch.setattr(orchestrator, "_execute_task_attempt", fake_execute)
    monkeypatch.setattr(orchestrator, "_run_review", lambda task, executions: ReviewReport(status="changes_requested", findings=[], summary="retry"))
    monkeypatch.setattr(orchestrator, "_run_verification", lambda task, executions: _verification_failed())
    monkeypatch.setattr(orchestrator.research_agent, "update_files", lambda changed_files: None)

    orchestrator._run_tiered_retry_loop(
        task_results=[_task_result()],
        verification_task=_verification_task(),
        verification=_verification_failed(),
        context=None,
        phase_name="Implementation Phase",
        run_id="run-5",
    )

    assert attempts["count"] == 3

