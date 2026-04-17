import os

from config import load_config
from models.project import TaskDocument
from runtime.router import BackendRouter


def _task(
    title: str = "Build",
    phase: str = "impl",
    selected_backend: str | None = None,
    model: str | None = None,
):
    return TaskDocument(
        task_id="task",
        title=title,
        description="x",
        phase=phase,
        selected_backend=selected_backend,
        model=model,
    )


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


def test_task_backend_override(monkeypatch):
    monkeypatch.delenv("BACKEND_OVERRIDE", raising=False)
    monkeypatch.setenv("ROUTING_MODE", "manual")
    config = load_config()
    router = BackendRouter(config)
    decision = router.select(_task(selected_backend="gemini_cli"))
    assert decision.backend_name == "gemini_cli"
    assert decision.reason == "task override"


def test_auto_routing_uses_profile_selected_model(monkeypatch):
    profile_model = "openrouter/meta-llama/llama-2-13b-chat"
    monkeypatch.setenv("ROUTING_MODE", "auto")
    monkeypatch.delenv("BACKEND_OVERRIDE", raising=False)
    monkeypatch.delenv("OPENROUTER_PREFERRED_MODELS", raising=False)
    config = load_config()
    router = BackendRouter(config)
    monkeypatch.setattr(router.model_profiles, "get_best_model", lambda *_args: profile_model)
    task = TaskDocument(
        task_id="task",
        title="Implement endpoint",
        description="Add coding changes across modules",
        phase="implementation",
        acceptance_criteria=["a", "b", "c"],
    )

    decision = router.select(task)

    assert decision.reason == f"auto: profile-selected model ({profile_model})"
    assert decision.backend_name == "aider_cli"
    assert decision.models == [profile_model]


def test_auto_routing_preferred_models_take_priority(monkeypatch):
    preferred_model = "openrouter/deepseek/deepseek-v3.2"
    monkeypatch.setenv("ROUTING_MODE", "auto")
    monkeypatch.delenv("BACKEND_OVERRIDE", raising=False)
    monkeypatch.setenv("OPENROUTER_PREFERRED_MODELS", preferred_model)
    config = load_config()
    router = BackendRouter(config)
    task = TaskDocument(
        task_id="task",
        title="Implement endpoint",
        description="Add coding changes across modules",
        phase="implementation",
        acceptance_criteria=["a", "b", "c"],
    )

    decision = router.select(task)

    assert decision.backend_name == "aider_cli"
    assert decision.models[0] == preferred_model


def test_manual_and_rules_routing_unchanged(monkeypatch):
    monkeypatch.setenv("ROUTING_MODE", "manual")
    monkeypatch.setenv("BACKEND_OVERRIDE", "aider_cli")
    config = load_config()
    router = BackendRouter(config)

    manual_decision = router.select(_task())
    assert manual_decision.backend_name == "aider_cli"

    monkeypatch.setenv("ROUTING_MODE", "rules")
    monkeypatch.delenv("BACKEND_OVERRIDE", raising=False)
    config = load_config()
    router = BackendRouter(config)

    rules_decision = router.select(_task(title="Refactor module"))
    assert rules_decision.backend_name == "aider_cli"


def test_task_model_override_appears_in_routing_decision(monkeypatch):
    model = "openrouter/deepseek/deepseek-v3.2"
    monkeypatch.setenv("ROUTING_MODE", "auto")
    monkeypatch.delenv("BACKEND_OVERRIDE", raising=False)
    monkeypatch.delenv("OPENROUTER_PREFERRED_MODELS", raising=False)
    config = load_config()
    router = BackendRouter(config)

    decision = router.select(_task(model=model))

    assert decision.backend_name == "aider_cli"
    assert decision.reason == f"task model override ({model})"
    assert decision.models == [model]
    assert decision.metadata["task_model"] == model


def test_task_model_none_falls_back_to_normal_auto_routing(monkeypatch):
    profile_model = "openrouter/meta-llama/llama-2-13b-chat"
    monkeypatch.setenv("ROUTING_MODE", "auto")
    monkeypatch.delenv("BACKEND_OVERRIDE", raising=False)
    monkeypatch.delenv("OPENROUTER_PREFERRED_MODELS", raising=False)
    config = load_config()
    router = BackendRouter(config)
    monkeypatch.setattr(router.model_profiles, "get_best_model", lambda *_args: profile_model)

    decision = router.select(_task(model=None))

    assert decision.reason == f"auto: profile-selected model ({profile_model})"
    assert decision.backend_name == "aider_cli"
    assert decision.models == [profile_model]
