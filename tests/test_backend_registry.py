from backends.registry import REGISTRY
from models.project import ContextPackage, TaskDocument


def test_registry_returns_backends():
    backend = REGISTRY.get("codex_cli")
    task = TaskDocument(task_id="t1", title="Implement", description="desc", phase="alpha")
    context = ContextPackage(summaries=["s"], files=[], notes="note")
    result = backend.execute(task, context)
    assert result.backend == "codex_cli"
    assert result.exit_code == 0


def test_registry_lists_backends():
    names = REGISTRY.names()
    assert {"codex_cli", "claude_code_cli", "gemini_cli", "aider_cli"}.issubset(set(names))
