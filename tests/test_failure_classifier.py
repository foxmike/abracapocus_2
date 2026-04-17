from models.reports import BackendExecution, VerificationCheck, VerificationReport
from runtime.failure_classifier import classify_failure


def _execution(stderr: str, exit_code: int = 1) -> BackendExecution:
    return BackendExecution(
        backend="codex_cli",
        command=["codex", "exec"],
        stdout="",
        stderr=stderr,
        exit_code=exit_code,
        duration_seconds=0.2,
    )


def test_syntax_error_classified_as_syntax_with_retry_likely_true():
    verification = VerificationReport(
        status="failed",
        checks=[
            VerificationCheck(
                name="pytest",
                status="failed",
                detail='File "app.py", line 3\nSyntaxError: invalid syntax',
            )
        ],
        notes="",
        profile="strict",
    )

    result = classify_failure(verification, [_execution("SyntaxError: invalid syntax")])

    assert result.failure_type == "syntax"
    assert result.retry_likely is True


def test_pytest_failure_extracts_test_name_into_failure_detail():
    verification = VerificationReport(
        status="failed",
        checks=[
            VerificationCheck(
                name="pytest",
                status="failed",
                detail="FAILED tests/test_math.py::test_add - AssertionError: assert 1 == 2",
            )
        ],
        notes="",
        profile="strict",
    )

    result = classify_failure(verification, [_execution("pytest FAILED")])

    assert result.failure_type == "test"
    assert "tests/test_math.py::test_add" in result.failure_detail
    assert "AssertionError" in result.failure_detail


def test_unknown_failure_second_occurrence_disables_retry_likely():
    verification = VerificationReport(
        status="failed",
        checks=[
            VerificationCheck(
                name="custom",
                status="failed",
                detail="tool crashed unexpectedly",
            )
        ],
        notes="",
        profile="strict",
    )
    first = _execution("non-diagnostic failure")
    second = _execution("non-diagnostic failure")

    result = classify_failure(verification, [first, second])

    assert result.failure_type == "unknown"
    assert result.retry_likely is False

