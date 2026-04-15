"""Aider CLI backend adapter."""
from __future__ import annotations

from pathlib import Path
from typing import List

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class AiderCliBackend(CodingBackend):
    name = "aider_cli"
    executable = "aider"

    def __init__(self, prompt_path: Path | None = None, timeout: int = 90, working_root: Path | None = None):
        super().__init__(
            prompt_path=prompt_path or Path("prompts/aider_cli.md"),
            working_root=working_root,
            timeout=timeout,
        )
        self.supports_direct_execution = True

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None) -> List[str]:
        command: List[str] = [
            self.executable,
            "--yes",
            "--no-auto-commits",
            "--root",
            str(self.workdir),
        ]
        if model:
            command += ["--model", model]
        message = task.description or task.title
        if context.agents_md:
            message += "\n\nAGENTS.md guidance:\n" + context.agents_md
        command += ["--message", message]
        for f in context.files[:5]:
            command += ["--file", f]
        if not context.files:
            command += ["--file", "README.md"]
        return command
