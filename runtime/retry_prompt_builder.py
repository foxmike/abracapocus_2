"""Build enriched retry tasks from prior failed attempts."""
from __future__ import annotations

from typing import Iterable, List

from models.project import TaskDocument
from models.reports import BackendExecution
from runtime.failure_classifier import FailureClassification


def build_retry_task(
    original_task: TaskDocument,
    classification: FailureClassification,
    attempts: Iterable[BackendExecution],
    attempt_number: int,
) -> TaskDocument:
    attempt_list = list(attempts)
    reference_attempt = _latest_failed_attempt(attempt_list)
    changed_files = _extract_changed_files(reference_attempt)

    lines: List[str] = [original_task.description.strip()]
    lines.extend(
        [
            "",
            f"Retry attempt: {attempt_number}",
            f"Failure type: {classification.failure_type}",
            f"Failure detail: {classification.failure_detail}",
            f"Suggested focus: {classification.suggested_focus}",
            "Do not repeat the same approach used in prior attempt(s).",
            "",
            "Last failed attempt stdout:",
            reference_attempt.stdout,
            "",
            "Last failed attempt stderr:",
            reference_attempt.stderr,
            "",
            "Files changed in last attempt:",
        ]
    )
    if changed_files:
        lines.extend([f"- {path}" for path in changed_files])
    else:
        lines.append("- none recorded")

    if attempt_number >= 2:
        diff_summary = reference_attempt.diff_summary.strip() or "No diff summary recorded"
        lines.extend(["", "Prior attempt diff summary:", diff_summary])

    updated_description = "\n".join(lines).strip()
    return original_task.model_copy(update={"description": updated_description})


def _latest_failed_attempt(attempts: List[BackendExecution]) -> BackendExecution:
    for attempt in reversed(attempts):
        if attempt.exit_code != 0:
            return attempt
    if not attempts:
        raise ValueError("At least one prior backend attempt is required")
    return attempts[-1]


def _extract_changed_files(execution: BackendExecution) -> List[str]:
    paths: List[str] = []
    for changed in execution.changed_files:
        if not isinstance(changed, dict):
            continue
        value = changed.get("path") or changed.get("file")
        if isinstance(value, str) and value and value not in paths:
            paths.append(value)
    return paths

