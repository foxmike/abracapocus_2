"""Task complexity scoring helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from models.project import TaskDocument
from runtime.router import _infer_task_type


@dataclass(slots=True)
class ComplexityScore:
    scope: str
    risk: str
    estimated_files: int
    recommended_phases: int
    recommended_backend: str


class ComplexityClassifier:
    """Classify tasks by scope/risk and recommend planning depth."""

    _HIGH_RISK_KEYWORDS = ("auth", "database", "api", "migration")
    _BACKEND_BY_TASK_TYPE = {
        "planning": "claude_code_cli",
        "review": "gemini_cli",
        "quick": "gemini_cli",
        "coding": "codex_cli",
    }

    def classify(
        self,
        title: str,
        description: str,
        acceptance_criteria: Sequence[str],
        context_files: Sequence[str],
    ) -> ComplexityScore:
        criteria_count = len(acceptance_criteria)
        description_text = description.strip()
        description_length = len(description_text)
        context_count = len(context_files)

        risk = self._risk_level(title, description, acceptance_criteria)
        scope = self._scope(criteria_count, description_length, risk)
        recommended_phases = {"micro": 1, "standard": 3, "complex": 5}[scope]
        estimated_files = self._estimate_files(scope, criteria_count, context_count)
        recommended_backend = self._recommended_backend(
            title=title,
            description=description,
            acceptance_criteria=acceptance_criteria,
        )

        return ComplexityScore(
            scope=scope,
            risk=risk,
            estimated_files=estimated_files,
            recommended_phases=recommended_phases,
            recommended_backend=recommended_backend,
        )

    def _risk_level(self, title: str, description: str, acceptance_criteria: Sequence[str]) -> str:
        combined_text = " ".join([title, description, *acceptance_criteria]).lower()
        if any(keyword in combined_text for keyword in self._HIGH_RISK_KEYWORDS):
            return "high"
        if len(acceptance_criteria) >= 4:
            return "medium"
        return "low"

    def _scope(self, criteria_count: int, description_length: int, risk: str) -> str:
        if criteria_count >= 5 or risk == "high":
            return "complex"
        if criteria_count == 1 and description_length < 100:
            return "micro"
        if 2 <= criteria_count <= 4:
            return "standard"
        return "standard"

    def _estimate_files(self, scope: str, criteria_count: int, context_count: int) -> int:
        if scope == "micro":
            return max(1, context_count or 1)
        if scope == "complex":
            return max(8, context_count, criteria_count * 2)
        return max(3, context_count, criteria_count * 2)

    def _recommended_backend(
        self,
        title: str,
        description: str,
        acceptance_criteria: Sequence[str],
    ) -> str:
        task = TaskDocument(
            task_id="complexity-classifier-temp",
            title=title,
            description=description,
            phase="implementation",
            acceptance_criteria=list(acceptance_criteria),
        )
        task_type = _infer_task_type(task)
        return self._BACKEND_BY_TASK_TYPE.get(task_type, "codex_cli")
