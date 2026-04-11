from pathlib import Path

from backends.base import CodingBackend
from backends.registry import REGISTRY
from models.project import ContextPackage, TaskDocument


def test_registry_returns_backends(monkeypatch):
    monkeypatch.setattr(CodingBackend, "_git_status_snapshot", lambda self, workdir: ({}, None))
    monkeypatch.setattr(CodingBackend, "_git_diff_summary", lambda self, workdir, paths: "")
    backend = REGISTRY.get("codex_cli")
    task = TaskDocument(task_id="t1", title="Implement", description="desc", phase="alpha")
    context = ContextPackage(summaries=["s"], files=[], notes="note")
    result = backend.execute(task, context, dry_run=True)
    assert result.backend == "codex_cli"
    assert result.exit_code == 0
    assert result.working_directory == str(Path.cwd())
    assert result.changed_files == []
    assert result.diff_summary in {"", "No file changes detected"}


def test_registry_lists_backends():
    names = REGISTRY.names()
    assert {"codex_cli", "claude_code_cli", "gemini_cli", "aider_cli", "demo_cli"}.issubset(set(names))
