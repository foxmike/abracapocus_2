import json
import os
import subprocess
from pathlib import Path

from config import load_config
from models.project import TaskDocument
from scripts import ops


def _blocked_payload(task_id: str = "resume-task") -> dict:
    task = TaskDocument(
        task_id=task_id,
        title="Resume Task",
        description="Original blocked task description",
        phase="phase_5",
        selected_backend="demo_cli",
        verification_profile="minimal",
    )
    return {
        "task": task.model_dump(mode="json"),
        "run_id": "blocked-run",
        "attempt_count": 2,
        "status": "blocked",
        "attempts": [
            {
                "backend": "codex_cli",
                "model": "codex",
                "exit_code": 1,
                "stdout": "attempt one stdout",
                "stderr": "attempt one stderr",
                "diff_summary": "a.py | 2 ++",
                "changed_files": [{"path": "a.py"}],
            },
            {
                "backend": "codex_cli",
                "model": "codex",
                "exit_code": 1,
                "stdout": "attempt two stdout",
                "stderr": "attempt two stderr",
                "diff_summary": "b.py | 3 ++-",
                "changed_files": [{"path": "b.py"}],
            },
        ],
    }


def test_task_resume_loads_blocked_report_and_creates_new_task(monkeypatch, tmp_path):
    config = load_config()
    config.paths = config.paths.model_copy(update={"reports_dir": tmp_path})
    blocked_path = tmp_path / "blocked-resume-task-abc.json"
    blocked_path.write_text(json.dumps(_blocked_payload()), encoding="utf-8")

    captured = {}

    class FakeReport:
        def model_dump_json(self, indent: int = 2) -> str:
            return json.dumps({"status": "ok"}, indent=indent)

    class FakeOrchestrator:
        def __init__(self, _config):
            pass

        def run(self, request, task):
            captured["request"] = request
            captured["task"] = task
            return FakeReport()

    monkeypatch.setattr(ops, "load_config", lambda: config)
    monkeypatch.setattr(ops, "SupervisorOrchestrator", FakeOrchestrator)

    ops.task_resume(task_id="resume-task", context="")

    assert captured["task"].task_id == "resume-task"
    assert isinstance(captured["task"], TaskDocument)
    assert captured["task"].status == "pending"


def test_resumed_task_description_includes_all_attempt_summaries(tmp_path):
    blocked_path = tmp_path / "blocked-resume-task-abc.json"
    payload = _blocked_payload()

    resumed = ops._task_from_blocked_payload(payload, blocked_path)

    assert "attempt one stdout" in resumed.description
    assert "attempt one stderr" in resumed.description
    assert "attempt two stdout" in resumed.description
    assert "attempt two stderr" in resumed.description
    assert "a.py" in resumed.description
    assert "b.py" in resumed.description


def test_make_task_resume_runs_without_error(tmp_path):
    task_id = "make-resume-task"
    result = subprocess.run(
        ["make", "-n", "task-resume", f"TASK={task_id}", "CONTEXT=resume-test"],
        cwd=Path.cwd(),
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "ABRACAPOCUS_ALLOW_MAIN": "true"},
    )

    assert result.returncode == 0, result.stderr or result.stdout
