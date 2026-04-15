"""Backend abstractions for CLI coding agents."""
from __future__ import annotations

import json
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from models.project import ContextPackage, TaskDocument

STATUS_LABELS = {
    "??": "untracked",
    "M": "modified",
    "A": "added",
    "D": "deleted",
    "R": "renamed",
    "C": "copied",
    "U": "updated_unmerged",
}


class SecurityError(RuntimeError):
    """Raised when backend execution escapes the configured working root."""


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
    working_directory: str | None = None
    changed_files: List[Dict[str, str]] = field(default_factory=list)
    diff_summary: str = ""


class CodingBackend:
    """Base class for CLI-backed coding agents."""

    name: str = "generic"
    executable: str = ""

    def __init__(self, prompt_path: Path, working_root: Path, timeout: int = 60):
        self.prompt_path = prompt_path
        self.prompt = Path(prompt_path).read_text(encoding="utf-8")
        self.timeout = timeout
        if working_root is None:
            raise ValueError("working_root is required for backend initialization")
        self.working_root = Path(working_root)
        self.workdir = self.working_root
        # Backends can opt-in to real CLI effects (writes, edits, etc.).
        self.supports_direct_execution = False

    def _check_workdir_safe(self) -> None:
        resolved_workdir = self.workdir.resolve()
        resolved_working_root = self.working_root.resolve()
        if resolved_workdir != resolved_working_root and resolved_working_root not in resolved_workdir.parents:
            raise SecurityError(
                f"Unsafe backend workdir: workdir={resolved_workdir} working_root={resolved_working_root}"
            )

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
        self._check_workdir_safe()
        workdir = str(self.workdir)
        before_snapshot, before_error = self._git_status_snapshot(workdir)
        real_execution = not dry_run and self._can_run_cli()
        if not real_execution:
            stdout = json.dumps(
                {
                    "task": task.model_dump(mode="json"),
                    "context_notes": context.notes,
                    "agents_metadata": context.agents_metadata,
                    "agents_md_applied": bool(context.agents_md.strip()),
                },
                indent=2,
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
                cwd=workdir,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            exit_code = proc.returncode
        duration = time.time() - start
        changed_files, diff_summary = self._collect_repo_deltas(workdir, before_snapshot, before_error)
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
            working_directory=workdir,
            changed_files=changed_files,
            diff_summary=diff_summary,
        )

    def _can_run_cli(self) -> bool:
        """Check whether the backing CLI executable is available."""

        return bool(self.executable and shutil.which(self.executable))

    def _git_status_snapshot(self, workdir: str) -> Tuple[Optional[Dict[str, str]], Optional[str]]:
        command = ["git", "status", "--porcelain"]
        try:
            proc = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                cwd=workdir,
            )
        except FileNotFoundError as exc:
            return None, str(exc)
        if proc.returncode != 0:
            detail = proc.stderr.strip() or proc.stdout.strip() or f"git status failed ({proc.returncode})"
            return None, detail
        snapshot: Dict[str, str] = {}
        for line in proc.stdout.splitlines():
            if not line.strip():
                continue
            code = line[:2]
            path = line[3:]
            snapshot[path] = code
        return snapshot, None

    def _collect_repo_deltas(
        self,
        workdir: str,
        before_snapshot: Optional[Dict[str, str]],
        before_error: Optional[str],
    ) -> Tuple[List[Dict[str, str]], str]:
        after_snapshot, after_error = self._git_status_snapshot(workdir)
        if before_snapshot is None or after_snapshot is None:
            reason = after_error or before_error or "git metadata unavailable"
            return [], f"git metadata unavailable: {reason}"
        changed: List[Dict[str, str]] = []
        for path, status_code in after_snapshot.items():
            previous = before_snapshot.get(path)
            if previous != status_code:
                changed.append(
                    {
                        "path": path,
                        "status": self._describe_status(status_code),
                        "code": status_code.strip() or status_code,
                    }
                )
        diff_summary = self._git_diff_summary(workdir, [item["path"] for item in changed])
        if not changed and not diff_summary:
            diff_summary = "No file changes detected"
        return changed, diff_summary

    def _describe_status(self, code: str) -> str:
        normalized = code.strip()
        return STATUS_LABELS.get(normalized, normalized)

    def _git_diff_summary(self, workdir: str, paths: List[str]) -> str:
        if not paths:
            return ""
        command = ["git", "diff", "--stat"] + paths
        try:
            proc = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                cwd=workdir,
            )
        except FileNotFoundError as exc:
            return f"git diff unavailable: {exc}"
        if proc.returncode != 0:
            detail = proc.stderr.strip() or proc.stdout.strip() or f"git diff failed ({proc.returncode})"
            return f"git diff unavailable: {detail}"
        summary = proc.stdout.strip()
        return summary or "git diff reported no changes"
