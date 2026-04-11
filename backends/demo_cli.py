"""Demo CLI backend adapter."""
from __future__ import annotations

from pathlib import Path
from typing import List

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class DemoCliBackend(CodingBackend):
    name = "demo_cli"
    executable = "python"

    def __init__(self, prompt_path: Path | None = None, timeout: int = 60):
        super().__init__(prompt_path or Path("prompts/demo_cli.md"), timeout)
        self.supports_direct_execution = True

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None) -> List[str]:
        notes = context.notes or ""
        return [
            self.executable,
            "scripts/demo_improvement.py",
            "--task-id",
            task.task_id,
            "--title",
            task.title,
            "--description",
            task.description or "",
            "--phase",
            task.phase or "",
            "--context-notes",
            notes,
        ]
