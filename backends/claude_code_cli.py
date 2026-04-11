"""Claude Code CLI backend adapter."""
from __future__ import annotations

from pathlib import Path
from typing import List

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class ClaudeCodeCliBackend(CodingBackend):
    name = "claude_code_cli"
    executable = "claude-code"

    def __init__(self, prompt_path: Path | None = None, timeout: int = 120):
        super().__init__(prompt_path or Path("prompts/claude_code_cli.md"), timeout)

    def build_command(self, task: TaskDocument, context: ContextPackage) -> List[str]:
        return [
            self.executable,
            "run",
            "--task",
            task.title,
            "--phase",
            task.phase,
            "--notes",
            context.notes,
        ]
