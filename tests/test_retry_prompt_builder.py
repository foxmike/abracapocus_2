from models.project import TaskDocument
from models.reports import BackendExecution
from runtime.failure_classifier import FailureClassification
from runtime.retry_prompt_builder import build_retry_task


def _task() -> TaskDocument:
    return TaskDocument(
        task_id="5.2",
        title="Retry prompt builder",
        description="Implement retry prompt enrichment.",
        phase="phase_5",
        acceptance_criteria=["criterion-a", "criterion-b"],
    )


def _attempt(stderr: str = "error", stdout: str = "out", diff_summary: str = "", exit_code: int = 1):
    return BackendExecution(
        backend="codex_cli",
        command=["codex", "exec"],
        stdout=stdout,
        stderr=stderr,
        exit_code=exit_code,
        duration_seconds=1.0,
        changed_files=[{"path": "runtime/retry_prompt_builder.py", "status": "modified", "code": "M"}],
        diff_summary=diff_summary,
    )


def _classification() -> FailureClassification:
    return FailureClassification(
        failure_type="test",
        affected_files=["tests/test_retry_prompt_builder.py"],
        failure_detail="FAILED tests/test_retry_prompt_builder.py::test_case - AssertionError",
        retry_likely=True,
        suggested_focus="Fix assertion mismatch",
    )


def test_retry_description_contains_failure_detail_from_classifier():
    result = build_retry_task(_task(), _classification(), [_attempt()], attempt_number=1)

    assert "FAILED tests/test_retry_prompt_builder.py::test_case - AssertionError" in result.description


def test_retry_description_contains_changed_files_from_prior_attempt():
    result = build_retry_task(_task(), _classification(), [_attempt()], attempt_number=1)

    assert "Files changed in last attempt:" in result.description
    assert "runtime/retry_prompt_builder.py" in result.description


def test_attempt_three_description_includes_diff_summary():
    result = build_retry_task(
        _task(),
        _classification(),
        [_attempt(diff_summary="runtime/retry_prompt_builder.py | 12 +++++++++---")],
        attempt_number=3,
    )

    assert "Prior attempt diff summary:" in result.description
    assert "runtime/retry_prompt_builder.py | 12 +++++++++---" in result.description


def test_original_acceptance_criteria_preserved_unchanged():
    task = _task()
    original_criteria = list(task.acceptance_criteria)

    result = build_retry_task(task, _classification(), [_attempt()], attempt_number=2)

    assert result.acceptance_criteria == original_criteria
    assert task.acceptance_criteria == original_criteria

