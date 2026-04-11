"""Verification agent."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Sequence

from agents.base import BaseAgent
from config import VerificationCheckSettings, VerificationSettings
from models.project import TaskDocument
from models.reports import BackendExecution, VerificationCheck, VerificationReport
from runtime.deep_agent_factory import DeepAgentFactory


class VerifierAgent(BaseAgent):
    def __init__(self, factory: DeepAgentFactory, verification_settings: VerificationSettings) -> None:
        super().__init__(
            name="verifier_agent",
            prompt_file="prompts/verifier.md",
            skills=["skills/verification", "skills/task_handoff"],
            factory=factory,
        )
        self.settings = verification_settings
        self.workdir = Path(self.settings.workdir)

    def verify(self, task: TaskDocument, execution: BackendExecution | Sequence[BackendExecution]) -> VerificationReport:
        executions = self._normalize(execution)
        primary = executions[0]
        response = self.invoke(
            {
                "task": task.model_dump(),
                "backend": primary.backend,
                "model": primary.model,
                "candidates": [item.model or item.backend for item in executions],
            }
        )
        profile_name = self._resolve_profile(task)
        checks = self._run_checks(profile_name)
        any_success = any(item.exit_code == 0 for item in executions)
        status = "passed" if any_success and all(c.status == "passed" for c in checks) else "failed"
        notes = response.get("notes") if isinstance(response, dict) else "Verification complete"
        return VerificationReport(status=status, checks=checks, notes=notes or "", profile=profile_name)

    def _run_checks(self, profile_name: str) -> List[VerificationCheck]:
        results: List[VerificationCheck] = []
        for check_settings in self.settings.active_checks(profile_name):
            results.append(self._run_check(check_settings))
        return results

    def _run_check(self, check_settings: VerificationCheckSettings) -> VerificationCheck:
        command = list(check_settings.command)
        try:
            proc = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                cwd=self.workdir,
            )
            detail = proc.stdout.strip() or proc.stderr.strip() or check_settings.description or "ok"
            status = "passed" if proc.returncode == 0 else "failed"
            exit_code = proc.returncode
        except FileNotFoundError as exc:
            # Command missing is deterministic failure with a clear message.
            detail = str(exc)
            status = "failed"
            exit_code = None
        return VerificationCheck(
            name=check_settings.name,
            status=status,
            detail=detail,
            command=command,
            exit_code=exit_code,
        )

    def _resolve_profile(self, task: TaskDocument) -> str:
        requested = task.verification_profile
        if requested and self.settings.has_profile(requested):
            return requested
        return self.settings.active_profile

    def _normalize(self, execution: BackendExecution | Sequence[BackendExecution]) -> List[BackendExecution]:
        if isinstance(execution, BackendExecution):
            return [execution]
        return list(execution)
