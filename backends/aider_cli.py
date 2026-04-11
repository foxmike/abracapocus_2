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

    def build_command(self, task: TaskDocument, context: ContextPackage) -> List[str]:
        return [
            self.executable,
            "--message",
            task.description,
            "--files",
            ",".join(context.files[:5]) or "README.md",
        ]
