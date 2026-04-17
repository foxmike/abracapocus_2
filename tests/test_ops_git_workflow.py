import json
import subprocess
from pathlib import Path

from config import load_config
from scripts import ops


def _git(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=path, capture_output=True, text=True, check=False)


def _init_repo(path: Path) -> None:
    _git(path, "init", "-b", "main")
    _git(path, "config", "user.email", "test@example.com")
    _git(path, "config", "user.name", "Test User")
    (path / "README.md").write_text("init\n", encoding="utf-8")
    _git(path, "add", "README.md")
    _git(path, "commit", "-m", "init")


def _config_for_repo(repo: Path):
    config = load_config()
    paths = config.paths.model_copy(
        update={
            "root_dir": repo,
            "reports_dir": repo / "reports",
            "state_file": repo / "state" / "runtime_state.json",
            "working_root": repo,
            "plans_dir": repo / "plans",
            "tasks_dir": repo / "tasks",
            "phases_dir": repo / "phases",
            "logs_dir": repo / "logs",
        }
    )
    paths.reports_dir.mkdir(parents=True, exist_ok=True)
    paths.state_file.parent.mkdir(parents=True, exist_ok=True)
    paths.plans_dir.mkdir(parents=True, exist_ok=True)
    paths.tasks_dir.mkdir(parents=True, exist_ok=True)
    paths.phases_dir.mkdir(parents=True, exist_ok=True)
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    config.paths = paths
    return config


def _write_run_report(repo: Path, task_id: str, branch_name: str) -> None:
    (repo / "reports").mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {
            "task_id": task_id,
            "branch_name": branch_name,
        }
    }
    (repo / "reports" / "run-test.json").write_text(json.dumps(payload), encoding="utf-8")


def test_branch_show_prints_branch_name_for_last_run(monkeypatch, tmp_path, capsys):
    _init_repo(tmp_path)
    _write_run_report(tmp_path, "t1", "abracapocus/t1-branch")
    config = _config_for_repo(tmp_path)
    monkeypatch.setattr(ops, "load_config", lambda: config)

    ops.branch_show()
    payload = json.loads(capsys.readouterr().out)

    assert payload["branch"] == "abracapocus/t1-branch"


def test_merge_merges_run_branch_with_no_ff(monkeypatch, tmp_path):
    _init_repo(tmp_path)
    _git(tmp_path, "checkout", "-b", "abracapocus/t2-branch")
    (tmp_path / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(tmp_path, "add", "feature.txt")
    _git(tmp_path, "commit", "-m", "feature")
    _git(tmp_path, "checkout", "main")
    _write_run_report(tmp_path, "t2", "abracapocus/t2-branch")

    config = _config_for_repo(tmp_path)
    monkeypatch.setattr(ops, "load_config", lambda: config)

    ops.merge(task_id="t2")

    parents = _git(tmp_path, "rev-list", "--parents", "-n", "1", "HEAD").stdout.strip().split()
    assert len(parents) == 3


def test_abandon_deletes_run_branch_and_returns_to_base(monkeypatch, tmp_path):
    _init_repo(tmp_path)
    _git(tmp_path, "checkout", "-b", "abracapocus/t3-branch")
    _git(tmp_path, "checkout", "main")
    _write_run_report(tmp_path, "t3", "abracapocus/t3-branch")

    config = _config_for_repo(tmp_path)
    monkeypatch.setattr(ops, "load_config", lambda: config)

    ops.abandon(task_id="t3")

    assert _git(tmp_path, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() == "main"
    assert _git(tmp_path, "rev-parse", "--verify", "refs/heads/abracapocus/t3-branch").returncode != 0


def test_git_targets_handle_no_repo_gracefully(monkeypatch, tmp_path, capsys):
    config = _config_for_repo(tmp_path)
    monkeypatch.setattr(ops, "load_config", lambda: config)

    ops.branch_show()
    assert "No git repository detected" in capsys.readouterr().out

    ops.merge(task_id="missing")
    assert "No git repository detected" in capsys.readouterr().out

    ops.abandon(task_id="missing")
    assert "No git repository detected" in capsys.readouterr().out


def test_base_branch_env_develop_routes_merge_to_develop(monkeypatch, tmp_path):
    _init_repo(tmp_path)
    _git(tmp_path, "checkout", "-b", "develop")
    _git(tmp_path, "checkout", "-b", "abracapocus/t4-branch")
    (tmp_path / "develop.txt").write_text("dev\n", encoding="utf-8")
    _git(tmp_path, "add", "develop.txt")
    _git(tmp_path, "commit", "-m", "dev work")
    _git(tmp_path, "checkout", "main")
    _write_run_report(tmp_path, "t4", "abracapocus/t4-branch")

    config = _config_for_repo(tmp_path)
    monkeypatch.setattr(ops, "load_config", lambda: config)
    monkeypatch.setenv("ABRACAPOCUS_BASE_BRANCH", "develop")

    ops.merge(task_id="t4")

    assert _git(tmp_path, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() == "develop"
