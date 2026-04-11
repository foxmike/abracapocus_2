"""Reviewer agent."""
from __future__ import annotations

from typing import List, Sequence

from agents.base import BaseAgent
from models.project import TaskDocument
from models.reports import BackendExecution, ReviewFinding, ReviewReport
from runtime.deep_agent_factory import DeepAgentFactory


class ReviewerAgent(BaseAgent):
    def __init__(self, factory: DeepAgentFactory) -> None:
        super().__init__(
            name="reviewer_agent",
            prompt_file="prompts/reviewer.md",
            skills=["skills/coding_standards", "skills/change_assessment"],
            factory=factory,
        )

    def review(self, task: TaskDocument, execution: BackendExecution | Sequence[BackendExecution]) -> ReviewReport:
        executions = self._normalize(execution)
        payload = {
            "task": task.model_dump(),
            "backends": [item.backend for item in executions],
            "models": [item.model for item in executions if item.model],
            "tags": {item.model: item.model_tags for item in executions if item.model},
        }
        response = self.invoke(payload)
        findings: List[ReviewFinding] = []
        status = "approved"
        for item in executions:
            if item.exit_code != 0:
                status = "changes_requested"
                findings.append(
                    ReviewFinding(
                        severity="high",
                        location=task.task_id,
                        detail=f"Backend exit code {item.exit_code} for model {item.model or item.backend}",
                    )
                )
            elif "TODO" in item.stdout:
                findings.append(
                    ReviewFinding(
                        severity="medium",
                        location="stdout",
                        detail=f"Execution output contains TODO for model {item.model or item.backend}",
                    )
                )
                status = "changes_requested"
        summary = response.get("summary") if isinstance(response, dict) else "LLM review"
        return ReviewReport(status=status, findings=findings, summary=summary or "Review complete")

    def _normalize(self, execution: BackendExecution | Sequence[BackendExecution]) -> List[BackendExecution]:
        if isinstance(execution, BackendExecution):
            return [execution]
        return list(execution)
