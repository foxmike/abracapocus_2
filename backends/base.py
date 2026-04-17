"""Backend abstractions for CLI coding agents."""
from __future__ import annotations

import json
import logging
import os
import random
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
RATE_LIMIT_KEYWORDS = [
    "rate limit",
    "ratelimit",
    "too many requests",
    "429",
    "quota exceeded",
]
LOGGER = logging.getLogger(__name__)


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
    model_attempts: List[str] = field(default_factory=list)


class CodingBackend:
    """Base class for CLI-backed coding agents."""

    name: str = "generic"
    executable: str = ""

    def __init__(
        self,
        prompt_path: Path,
        working_root: Path,
        timeout: int = 60,
        max_retries: int = 3,
        retry_delay_base: float = 2.0,
    ):
        self.prompt_path = prompt_path
        self.prompt = self._load_prompt_with_non_interactive_header(Path(prompt_path))
        self.timeout = timeout
        self.max_retries = max(0, int(max_retries))
        self.retry_delay_base = max(0.0, float(retry_delay_base))
        self.min_seconds_between_calls, self.max_calls_per_minute = self._pace_settings_from_env()
        self.last_call_time: float | None = None
        self._call_timestamps: List[float] = []
        if working_root is None:
            raise ValueError("working_root is required for backend initialization")
        self.working_root = Path(working_root)
        self.workdir = self.working_root
        # Backends can opt-in to real CLI effects (writes, edits, etc.).
        self.supports_direct_execution = False

    def _load_prompt_with_non_interactive_header(self, prompt_path: Path) -> str:
        prompt_text = prompt_path.read_text(encoding="utf-8")
        header_path = prompt_path.parent / "shared" / "non_interactive_header.md"
        if not header_path.exists():
            return prompt_text
        header_text = header_path.read_text(encoding="utf-8").strip()
        if not header_text:
            return prompt_text
        if prompt_text.startswith(header_text):
            return prompt_text
        return f"{header_text}\n\n{prompt_text}"

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
        model: str | List[str] | None = None,
        model_tags: List[str] | None = None,
        task_type: str | None = None,
    ) -> BackendResult:
        requested_models = self._requested_models(model)
        command = self.build_command(task, context, model=requested_models[0])
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
            chosen_model = requested_models[0]
            model_attempts = [self._model_label(chosen_model)]
        else:
            stdout = ""
            stderr = ""
            exit_code = 1
            retry_count = 0
            total_retry_count = 0
            chosen_model = requested_models[0]
            model_attempts = []
            for model_name in requested_models:
                chosen_model = model_name
                model_attempts.append(self._model_label(model_name))
                command = self.build_command(task, context, model=model_name)
                stdout, stderr, exit_code, retry_count = self._run_with_retries(command, workdir)
                total_retry_count += retry_count
                if exit_code == 0:
                    break
            LOGGER.info("backend=%s retry_count=%d", self.name, total_retry_count)
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
            model=chosen_model,
            model_tags=model_tags or [],
            task_type=task_type,
            working_directory=workdir,
            changed_files=changed_files,
            diff_summary=diff_summary,
            model_attempts=model_attempts,
        )

    def _requested_models(self, model: str | List[str] | None) -> List[str | None]:
        if isinstance(model, list):
            return model or [None]
        return [model]

    def _model_label(self, model: str | None) -> str:
        return model if model else "default"

    def _run_with_retries(self, command: List[str], workdir: str) -> tuple[str, str, int, int]:
        retry_count = 0
        while True:
            try:
                self._enforce_pace()
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
                if exit_code == 0:
                    return stdout, stderr, exit_code, retry_count
                if exit_code == 2:
                    return stdout, stderr, exit_code, retry_count
                if not self._should_retry_from_process(exit_code, stderr):
                    return stdout, stderr, exit_code, retry_count
            except subprocess.TimeoutExpired as exc:
                stdout = self._decode_timeout_output(exc.stdout)
                stderr = self._decode_timeout_output(exc.stderr) or str(exc)
                exit_code = 1
                if retry_count >= self.max_retries:
                    return stdout, stderr, exit_code, retry_count
            except FileNotFoundError as exc:
                return "", str(exc), 1, retry_count
            except ConnectionError as exc:
                stdout = ""
                stderr = str(exc)
                exit_code = 1
                if retry_count >= self.max_retries:
                    return stdout, stderr, exit_code, retry_count

            if retry_count >= self.max_retries:
                return stdout, stderr, exit_code, retry_count
            delay = self.retry_delay_base * (2**retry_count) + random.random()
            LOGGER.info("backend=%s retry=%d delay_seconds=%.2f", self.name, retry_count + 1, delay)
            time.sleep(delay)
            retry_count += 1

    def _should_retry_from_process(self, exit_code: int, stderr: str) -> bool:
        if exit_code != 1:
            return False
        lowered = (stderr or "").lower()
        return any(keyword in lowered for keyword in RATE_LIMIT_KEYWORDS)

    def _decode_timeout_output(self, value: str | bytes | None) -> str:
        if value is None:
            return ""
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="ignore")
        return value

    def _pace_settings_from_env(self) -> tuple[float, int]:
        prefix = ""
        if self.name == "aider_cli":
            prefix = "AIDER"
        elif self.name == "gemini_cli":
            prefix = "GEMINI"
        elif self.name == "codex_cli":
            prefix = "CODEX"
        elif self.name == "claude_code_cli":
            prefix = "CLAUDE"
        if not prefix:
            return 0.0, 0
        min_delay = float(os.getenv(f"{prefix}_MIN_DELAY", "0"))
        max_per_minute = int(os.getenv(f"{prefix}_MAX_CALLS_PER_MINUTE", "0"))
        return max(0.0, min_delay), max(0, max_per_minute)

    def _enforce_pace(self) -> None:
        now = time.time()
        if self.min_seconds_between_calls > 0 and self.last_call_time is not None:
            elapsed = now - self.last_call_time
            wait_seconds = self.min_seconds_between_calls - elapsed
            if wait_seconds > 0:
                LOGGER.info("backend=%s pace_delay_seconds=%.2f", self.name, wait_seconds)
                time.sleep(wait_seconds)
                now += wait_seconds
        if self.max_calls_per_minute > 0:
            cutoff = now - 60
            self._call_timestamps = [stamp for stamp in self._call_timestamps if stamp > cutoff]
            if len(self._call_timestamps) >= self.max_calls_per_minute:
                oldest = self._call_timestamps[0]
                wait_seconds = 60 - (now - oldest)
                if wait_seconds > 0:
                    LOGGER.info("backend=%s pace_delay_seconds=%.2f", self.name, wait_seconds)
                    time.sleep(wait_seconds)
                    now += wait_seconds
                    cutoff = now - 60
                    self._call_timestamps = [stamp for stamp in self._call_timestamps if stamp > cutoff]
        self.last_call_time = now
        self._call_timestamps.append(now)

    def _can_run_cli(self) -> bool:
        """Check whether the backing CLI executable is available."""
        if os.getenv("DEEP_AGENT_MOCK_MODE", "").lower() in {"1", "true", "yes", "on"}:
            return False
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
