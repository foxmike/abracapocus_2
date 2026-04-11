"""Codex CLI backend adapter."""
from __future__ import annotations

from pathlib import Path
from typing import List

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class CodexCliBackend(CodingBackend):
    name = "codex_cli"
    executable = "codex"

    def __init__(self, prompt_path: Path | None = None, timeout: int = 90):
        super().__init__(prompt_path or Path("prompts/codex_cli.md"), timeout)

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None) -> List[str]:
        command = [
            self.executable,
            "task",
            "--id",
            task.task_id,
            "--title",
            task.title,
            "--phase",
            task.phase,
            "--context",
            context.notes,
        ]
        if task.acceptance_criteria:
            command += ["--acceptance", ";".join(task.acceptance_criteria)]
        return command
