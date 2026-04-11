"""Backend abstractions for CLI coding agents."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from models.project import ContextPackage, TaskDocument


@dataclass(slots=True)
class BackendResult:
    backend: str
    command: List[str]
    stdout: str
    stderr: str
    exit_code: int
    duration_seconds: float
    prompt_used: str
    model: str | None = None
    model_tags: List[str] = field(default_factory=list)
    task_type: str | None = None


class CodingBackend:
    """Base class for CLI-backed coding agents."""

    name: str = "generic"
    executable: str = ""

    def __init__(self, prompt_path: Path, timeout: int = 60):
        self.prompt_path = prompt_path
        self.prompt = Path(prompt_path).read_text(encoding="utf-8")
        self.timeout = timeout

    def build_command(self, task: TaskDocument, context: ContextPackage, model: str | None = None) -> List[str]:
        """Construct the CLI command for the backend."""

        return [self.executable, "--task", task.title, "--phase", task.phase]

    def execute(
        self,
        task: TaskDocument,
        context: ContextPackage,
        dry_run: bool = True,
        model: str | None = None,
        model_tags: List[str] | None = None,
        task_type: str | None = None,
    ) -> BackendResult:
        command = self.build_command(task, context, model=model)
        start = time.time()
        if dry_run or not self.executable:
            stdout = json.dumps(
                {"task": task.model_dump(mode="json"), "context_notes": context.notes}, indent=2
            )
            stderr = ""
            exit_code = 0
        else:
            import subprocess

            proc = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            exit_code = proc.returncode
        duration = time.time() - start
        return BackendResult(
            backend=self.name,
            command=command,
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            duration_seconds=duration,
            prompt_used=self.prompt,
            model=model,
            model_tags=model_tags or [],
            task_type=task_type,
        )
