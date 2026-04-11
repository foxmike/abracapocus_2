import os

from config import load_config
from models.project import TaskDocument
from runtime.router import BackendRouter


def _task(title: str = "Build", phase: str = "impl"):
    return TaskDocument(task_id="task", title=title, description="x", phase=phase)


def test_manual_routing_override(monkeypatch):
    monkeypatch.setenv("BACKEND_OVERRIDE", "aider_cli")
    config = load_config()
    router = BackendRouter(config)
    decision = router.select(_task())
    assert decision.backend_name == "aider_cli"


def test_rules_based(monkeypatch):
    monkeypatch.setenv("ROUTING_MODE", "rules")
    monkeypatch.delenv("BACKEND_OVERRIDE", raising=False)
    config = load_config()
    router = BackendRouter(config)
    decision = router.select(_task(title="Refactor module"))
    assert decision.backend_name == "aider_cli"
