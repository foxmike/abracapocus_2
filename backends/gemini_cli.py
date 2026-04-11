"""Gemini CLI backend adapter."""
from __future__ import annotations

from pathlib import Path
from typing import List

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class GeminiCliBackend(CodingBackend):
    name = "gemini_cli"
    executable = "gemini"

    def __init__(self, prompt_path: Path | None = None, timeout: int = 90):
        super().__init__(prompt_path or Path("prompts/gemini_cli.md"), timeout)

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None) -> List[str]:
        return [
            self.executable,
            "code",
            "--project",
            task.phase,
            "--task",
            task.task_id,
            "--summary",
            task.description,
        ]
