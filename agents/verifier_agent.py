"""Verification agent."""
from __future__ import annotations

import subprocess

from agents.base import BaseAgent
from models.project import TaskDocument
from models.reports import BackendExecution, VerificationCheck, VerificationReport
from runtime.deep_agent_factory import DeepAgentFactory


class VerifierAgent(BaseAgent):
    def __init__(self, factory: DeepAgentFactory) -> None:
        super().__init__(
            name="verifier_agent",
            prompt_file="prompts/verifier.md",
            skills=["skills/verification", "skills/task_handoff"],
            factory=factory,
        )

    def verify(self, task: TaskDocument, execution: BackendExecution) -> VerificationReport:
        response = self.invoke({"task": task.model_dump(), "backend": execution.backend})
        checks = [self._compile_check()]
        status = "passed" if execution.exit_code == 0 and all(c.status == "passed" for c in checks) else "failed"
        notes = response.get("notes") if isinstance(response, dict) else "Verification complete"
        return VerificationReport(status=status, checks=checks, notes=notes or "")

    def _compile_check(self) -> VerificationCheck:
        try:
            subprocess.run([
                "python",
                "-m",
                "py_compile",
                "main.py",
            ], check=True, capture_output=True)
            return VerificationCheck(name="py_compile", status="passed", detail="main.py compiles")
        except subprocess.CalledProcessError as exc:  # pragma: no cover
            return VerificationCheck(name="py_compile", status="failed", detail=exc.stderr or "compile error")
