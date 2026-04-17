"""Gemini CLI backend adapter."""
from __future__ import annotations

from pathlib import Path
from typing import List

from backends.base import CodingBackend
from models.project import ContextPackage, TaskDocument


class GeminiCliBackend(CodingBackend):
    name = "gemini_cli"
    executable = "gemini"

    def __init__(self, prompt_path: Path | None = None, timeout: int = 90, working_root: Path | None = None):
        super().__init__(
            prompt_path=prompt_path or Path("prompts/gemini_cli.md"),
            working_root=working_root,
            timeout=timeout,
        )
        self.supports_direct_execution = True

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None) -> List[str]:
        summary = task.description
        if context.agents_md:
            summary = f"{task.description}\n\nAGENTS.md guidance:\n{context.agents_md}"
        prompt = (
            f"Task: {task.title}\n"
            f"Phase: {task.phase}\n"
            f"Description: {summary}\n"
            f"Context: {context.notes}\n"
        )
        command = [
            self.executable,
            "--prompt",
            prompt,
            "--output-format",
            "json",
            "--include-directories",
            str(self.workdir),
            "--yolo",
            "--approval-mode",
            "yolo",
        ]
        if model:
            command.extend(["--model", model])
        return command
