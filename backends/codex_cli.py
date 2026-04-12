"""Codex CLI backend adapter."""
from __future__ import annotations

from pathlib import Path
from typing import List

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class CodexCliBackend(CodingBackend):
    name = "codex_cli"
    executable = "codex"

    def __init__(self, prompt_path: Path | None = None, timeout: int = 300):
        super().__init__(prompt_path or Path("prompts/codex_cli.md"), timeout)
        # Codex is the first backend allowed to perform real repository edits,
        # so we opt into direct execution (orchestrator will disable dry runs).
        self.supports_direct_execution = True

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None) -> List[str]:
        command = [self.executable, "exec", "--full-auto"]
        if model:
            command += ["-m", model]
        prompt = f"Task: {task.title}\n"
        if task.description:
            prompt += f"Description: {task.description}\n"
        if task.phase:
            prompt += f"Phase: {task.phase}\n"
        if task.acceptance_criteria:
            prompt += "Acceptance criteria:\n"
            for criterion in task.acceptance_criteria:
                prompt += f"  - {criterion}\n"
        if context.notes:
            prompt += f"Context: {context.notes}\n"
        command.append(prompt)
        return command
