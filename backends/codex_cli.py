"""Codex CLI backend adapter."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class CodexCliBackend(CodingBackend):
    name = "codex_cli"
    executable = "codex"

    def __init__(
        self,
        prompt_path: Path | None = None,
        timeout: int = 300,
        default_model: str | None = None,
        working_root: Path | None = None,
    ):
        super().__init__(
            prompt_path=prompt_path or Path("prompts/codex_cli.md"),
            working_root=working_root,
            timeout=timeout,
        )
        # Codex is the first backend allowed to perform real repository edits,
        # so we opt into direct execution (orchestrator will disable dry runs).
        self.supports_direct_execution = True
        self.default_model = default_model or os.getenv("CODEX_MODEL", "gpt-5.3-codex")

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None) -> List[str]:
        command = [
            self.executable,
            "exec",
            "--full-auto",
            "-C",
            str(self.workdir),
        ]
        effective_model = model or self.default_model
        if effective_model:
            command += ["-m", effective_model]
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
        if context.agents_md:
            prompt += "AGENTS.md:\n"
            prompt += f"{context.agents_md}\n"
        if context.agents_metadata:
            prompt += "AGENTS metadata:\n"
            prompt += f"{json.dumps(context.agents_metadata, sort_keys=True)}\n"
        command.append(prompt)
        return command
