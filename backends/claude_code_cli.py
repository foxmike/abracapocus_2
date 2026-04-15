"""Claude Code CLI backend adapter."""
from __future__ import annotations

from pathlib import Path
from typing import List

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class ClaudeCodeCliBackend(CodingBackend):
    name = "claude_code_cli"
    executable = "claude-code"

    def __init__(self, prompt_path: Path | None = None, timeout: int = 120, working_root: Path | None = None):
        super().__init__(
            prompt_path=prompt_path or Path("prompts/claude_code_cli.md"),
            working_root=working_root,
            timeout=timeout,
        )

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None) -> List[str]:
        notes = context.notes
        if context.agents_md:
            notes = f"{notes}\n\nAGENTS.md guidance:\n{context.agents_md}" if notes else f"AGENTS.md guidance:\n{context.agents_md}"
        return [
            self.executable,
            "run",
            "--task",
            task.title,
            "--phase",
            task.phase,
            "--notes",
            notes,
        ]
