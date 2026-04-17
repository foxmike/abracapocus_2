"""Git utility wrapper used by orchestration and operational commands."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import List


class GitManager:
    def __init__(self, repo_root: Path | str = ".") -> None:
        self.repo_root = Path(repo_root)
        self.base_branch = os.getenv("ABRACAPOCUS_BASE_BRANCH", "main")

    def create_branch(self, branch_name: str) -> bool:
        if not branch_name:
            return False
        if self.branch_exists(branch_name):
            result = self._run_git(["checkout", branch_name])
            return bool(result and result.returncode == 0)
        result = self._run_git(["checkout", "-b", branch_name])
        return bool(result and result.returncode == 0)

    def current_branch(self) -> str:
        result = self._run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        if not result or result.returncode != 0:
            return ""
        return result.stdout.strip()

    def commit_changes(self, message: str) -> bool:
        if not message or not self.get_changed_files():
            return False
        add = self._run_git(["add", "-A"])
        if not add or add.returncode != 0:
            return False
        commit = self._run_git(["commit", "-m", message])
        return bool(commit and commit.returncode == 0)

    def branch_exists(self, branch_name: str) -> bool:
        if not branch_name:
            return False
        result = self._run_git(["rev-parse", "--verify", f"refs/heads/{branch_name}"])
        return bool(result and result.returncode == 0)

    def get_changed_files(self) -> List[str]:
        result = self._run_git(["status", "--porcelain"])
        if not result or result.returncode != 0:
            return []
        files: List[str] = []
        for line in result.stdout.splitlines():
            if len(line) < 4:
                continue
            path = line[3:].strip()
            if path and path not in files:
                files.append(path)
        return files

    def safe_to_run(self) -> bool:
        current = self.current_branch()
        if not current:
            return False
        return current not in {"main", "master"}

    def _run_git(self, args: List[str]) -> subprocess.CompletedProcess[str] | None:
        if not self._is_git_repo_root():
            return None
        try:
            return subprocess.run(
                ["git", *args],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=False,
            )
        except (FileNotFoundError, NotADirectoryError):
            return None

    def _is_git_repo_root(self) -> bool:
        git_dir = self.repo_root / ".git"
        return git_dir.exists()
