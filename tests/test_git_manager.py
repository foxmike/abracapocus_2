import subprocess
from pathlib import Path

from runtime.git_manager import GitManager


def _init_repo(path: Path, branch: str = "main") -> None:
    subprocess.run(["git", "init", "-b", branch], cwd=path, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=path, check=True)
    (path / "README.md").write_text("init\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=path, check=True, capture_output=True, text=True)


def test_create_branch_creates_and_checks_out_branch(tmp_path):
    _init_repo(tmp_path)
    manager = GitManager(tmp_path)

    created = manager.create_branch("abracapocus/test-branch")

    assert created is True
    assert manager.current_branch() == "abracapocus/test-branch"


def test_commit_changes_stages_all_and_commits_message(tmp_path):
    _init_repo(tmp_path)
    manager = GitManager(tmp_path)
    manager.create_branch("abracapocus/commit-test")
    (tmp_path / "file.txt").write_text("change\n", encoding="utf-8")

    committed = manager.commit_changes("commit message")

    assert committed is True
    result = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stdout.strip() == "commit message"


def test_safe_to_run_false_on_main_or_master(tmp_path):
    _init_repo(tmp_path, branch="main")
    manager_main = GitManager(tmp_path)
    assert manager_main.safe_to_run() is False

    tmp_path_master = tmp_path / "master-repo"
    tmp_path_master.mkdir(parents=True, exist_ok=True)
    _init_repo(tmp_path_master, branch="master")
    manager_master = GitManager(tmp_path_master)
    assert manager_master.safe_to_run() is False


def test_methods_handle_git_not_initialized_gracefully(tmp_path):
    manager = GitManager(tmp_path)

    assert manager.current_branch() == ""
    assert manager.branch_exists("x") is False
    assert manager.create_branch("x") is False
    assert manager.get_changed_files() == []
    assert manager.commit_changes("msg") is False
    assert manager.safe_to_run() is False

