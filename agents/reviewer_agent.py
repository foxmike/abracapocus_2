"""Reviewer agent."""
from __future__ import annotations

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

    def review(self, task: TaskDocument, execution: BackendExecution) -> ReviewReport:
        response = self.invoke({"task": task.model_dump(), "backend": execution.backend})
        findings = []
        status = "approved"
        if execution.exit_code != 0:
            status = "changes_requested"
            findings.append(
                ReviewFinding(
                    severity="high",
                    location=task.task_id,
                    detail=f"Backend exit code {execution.exit_code}",
                )
            )
        elif "TODO" in execution.stdout:
            findings.append(
                ReviewFinding(
                    severity="medium",
                    location="stdout",
                    detail="Execution output contains TODO",
                )
            )
            status = "changes_requested"
        summary = response.get("summary") if isinstance(response, dict) else "LLM review"
        return ReviewReport(status=status, findings=findings, summary=summary or "Review complete")
