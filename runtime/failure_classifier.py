"""Failure classification helpers for verification and backend failures."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Iterable, List

from models.reports import BackendExecution, VerificationReport


_FILE_PATTERN = re.compile(r'File "([^"]+)"')
_PYTEST_FAILED_PATTERN = re.compile(r"FAILED\s+([^\s]+)::([^\s]+)\s+-\s+(.+)")
_PYTEST_NODE_PATTERN = re.compile(r"([\w./-]+\.py::[\w\[\]-]+)")


@dataclass(frozen=True)
class FailureClassification:
    failure_type: str
    affected_files: List[str]
    failure_detail: str
    retry_likely: bool
    suggested_focus: str

    def as_dict(self) -> dict:
        return asdict(self)


def classify_failure(
    verification: VerificationReport,
    executions: Iterable[BackendExecution],
) -> FailureClassification:
    execution_list = list(executions)
    failure_signatures = [
        _signature(item) for item in execution_list if item.exit_code != 0 and _signature(item)
    ]
    latest_signature = failure_signatures[-1] if failure_signatures else ""
    repeated_count = failure_signatures.count(latest_signature) if latest_signature else 0

    details = [check.detail for check in verification.checks if check.status == "failed" and check.detail]
    execution_stderr = [item.stderr for item in execution_list if item.exit_code != 0 and item.stderr]
    execution_stdout = [item.stdout for item in execution_list if item.exit_code != 0 and item.stdout]
    corpus = "\n".join(details + execution_stderr + execution_stdout)
    lowered = corpus.lower()
    affected_files = sorted(set(_extract_affected_files(corpus, execution_list)))
    failure_type = "unknown"
    failure_detail = ""
    retry_likely = True
    suggested_focus = "Inspect stderr/stdout and narrow the likely root cause before retrying."
    if "syntaxerror" in lowered:
        failure_type = "syntax"
        failure_detail = _extract_line(corpus, "SyntaxError") or "SyntaxError detected"
        suggested_focus = "Fix syntax issues in the referenced file and line."
    elif "module not found" in lowered or "modulenotfounderror" in lowered or "importerror" in lowered:
        failure_type = "import"
        failure_detail = (
            _extract_line(corpus, "ModuleNotFoundError")
            or _extract_line(corpus, "ImportError")
            or "Import failure detected"
        )
        suggested_focus = "Fix import paths or ensure required modules/files exist."
    else:
        pytest_failure = _extract_pytest_failure(corpus)
        if pytest_failure:
            failure_type = "test"
            failure_detail = pytest_failure
            suggested_focus = "Address the failing test assertion and related implementation path."
        elif "filenotfounderror" in lowered:
            failure_type = "missing_file"
            failure_detail = _extract_line(corpus, "FileNotFoundError") or "Missing file detected"
            suggested_focus = "Create the missing file or correct the referenced path."

    if failure_type == "unknown":
        failed_attempts = sum(1 for item in execution_list if item.exit_code != 0)
        retry_likely = failed_attempts < 2
        failure_detail = _first_non_empty(_extract_line(corpus, "FAILED"), latest_signature, "Unclassified failure")

    if (
        failure_type in {"syntax", "import", "test", "missing_file"}
        and latest_signature
        and repeated_count >= 2
    ):
        failure_type = "logic"
        failure_detail = _first_non_empty(latest_signature, failure_detail, "Repeated failure across attempts")
        retry_likely = False
        suggested_focus = "Change implementation strategy instead of repeating the same fix."

    return FailureClassification(
        failure_type=failure_type,
        affected_files=affected_files,
        failure_detail=failure_detail,
        retry_likely=retry_likely,
        suggested_focus=suggested_focus,
    )


def _signature(execution: BackendExecution) -> str:
    signature = execution.stderr.strip() or execution.stdout.strip()
    if not signature:
        return ""
    return signature.splitlines()[-1].strip()


def _extract_affected_files(corpus: str, executions: List[BackendExecution]) -> List[str]:
    files: List[str] = []
    files.extend(_FILE_PATTERN.findall(corpus))
    for node in _PYTEST_NODE_PATTERN.findall(corpus):
        files.append(node.split("::", 1)[0])
    for execution in executions:
        for changed_file in execution.changed_files:
            if not isinstance(changed_file, dict):
                continue
            file_path = changed_file.get("path") or changed_file.get("file")
            if isinstance(file_path, str) and file_path:
                files.append(file_path)
    return files


def _extract_pytest_failure(text: str) -> str:
    match = _PYTEST_FAILED_PATTERN.search(text)
    if match:
        return f"{match.group(1)}::{match.group(2)} - {match.group(3)}"
    test_header = re.search(r"_{2,}\s*([^\s]+)\s*_{2,}", text)
    assertion_line = re.search(r"^E\s+(.+)$", text, flags=re.MULTILINE)
    if test_header and assertion_line:
        return f"{test_header.group(1)} - {assertion_line.group(1)}"
    if "failed" in text.lower() and "pytest" in text.lower():
        return _extract_line(text, "FAILED") or "Pytest failure detected"
    return ""


def _extract_line(text: str, token: str) -> str:
    token_lower = token.lower()
    for line in text.splitlines():
        if token_lower in line.lower():
            return line.strip()
    return ""


def _first_non_empty(*values: str) -> str:
    for value in values:
        if value:
            return value
    return ""
