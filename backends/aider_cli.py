"""Aider CLI backend adapter."""
from __future__ import annotations

from pathlib import Path
from typing import List

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class AiderCliBackend(CodingBackend):
    name = "aider_cli"
    executable = "aider"

    def __init__(self, prompt_path: Path | None = None, timeout: int = 90):
        super().__init__(prompt_path or Path("prompts/aider_cli.md"), timeout)
        self.supports_direct_execution = True

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None) -> List[str]:
        command: List[str] = [
            self.executable,
            "--yes",
            "--no-auto-commits",
        ]
        if model:
            command += ["--model", model]
        command += ["--message", task.description or task.title]
        for f in context.files[:5]:
            command += ["--file", f]
        if not context.files:
            command += ["--file", "README.md"]
        return command
