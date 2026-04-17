"""Backend routing policies."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from backends.openrouter_models import OPENROUTER_MODELS
from backends.registry import REGISTRY
from config import AppConfig
from models.project import TaskDocument
from runtime.model_profile_store import ModelProfileStore

TASK_TYPE_TAGS = {
    "coding": ["coding_strong", "coding"],
    "planning": ["reasoning_strong"],
    "review": ["reasoning", "reasoning_strong"],
    "quick": ["cheap_fast"],
}


def _infer_task_type(task: TaskDocument) -> str:
    phase = (task.phase or "").lower()
    descriptor = f"{task.title} {task.description}".lower()
    if "research" in phase or "plan" in phase or "design" in descriptor:
        return "planning"
    if "verify" in phase or "review" in phase or "qa" in descriptor:
        return "review"
    if len(task.acceptance_criteria) <= 1 and len(task.description or "") < 160:
        return "quick"
    return "coding"


def _infer_task_complexity(task: TaskDocument) -> str:
    criteria_count = len(task.acceptance_criteria)
    description_length = len(task.description or "")
    if criteria_count >= 5 or description_length >= 320:
        return "high"
    if criteria_count >= 3 or description_length >= 180:
        return "medium"
    return "low"


def select_openrouter_model(task: TaskDocument) -> List[dict]:
    """Select the best OpenRouter models for the task."""

    from backends.openrouter_models import get_preferred_models

    preferred = get_preferred_models()
    if preferred:
        results = []
        model_map = {m["name"]: m for m in OPENROUTER_MODELS}
        for name in preferred:
            if name in model_map:
                results.append(model_map[name])
        if results:
            task_type = _infer_task_type(task)
            limit = 2 if task_type == "coding" else 1
            return results[:limit]

    # fall through to existing tag-based selection
    task_type = _infer_task_type(task)
    preferred_tags = TASK_TYPE_TAGS.get(task_type, ["coding_strong"])
    ranked: List[tuple[int, int, int, dict]] = []
    preferred_tag_set = set(preferred_tags)
    for idx, model in enumerate(OPENROUTER_MODELS):
        tags = set(model["tags"])
        match_score = len(tags & preferred_tag_set)
        cheap_bonus = 1 if task_type == "quick" and "cheap_fast" in tags else 0
        score = match_score * 10 + cheap_bonus
        ranked.append((score, model["context"], idx, model))
    ranked.sort(key=lambda entry: (-entry[0], -entry[1], entry[2]))
    filtered = [entry[3] for entry in ranked if entry[0] > 0]
    if not filtered:
        filtered = [entry[3] for entry in ranked]
    limit = 2 if task_type == "coding" else 1
    return filtered[:limit]


def _record_for_model(model_name: str, context_size: int = 0) -> dict:
    model_map = {model["name"]: model for model in OPENROUTER_MODELS}
    return model_map.get(model_name, {"name": model_name, "tags": [], "context": context_size})


@dataclass(slots=True)
class RoutingDecision:
    backend_name: str
    reason: str
    metadata: Dict[str, Any]
    models: List[str] = field(default_factory=list)
    model_tags: Dict[str, List[str]] = field(default_factory=dict)
    task_type: str | None = None

    def backend(self, working_root: Path):
        return REGISTRY.get(self.backend_name, working_root=working_root)


class BackendRouter:
    """Simple routing policy manager."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.model_profiles = ModelProfileStore()

    def select(self, task: TaskDocument) -> RoutingDecision:
        routing_mode = self.config.routing.routing_mode
        metadata: Dict[str, Any] = {"routing_mode": routing_mode}
        task_type = _infer_task_type(task)
        metadata["task_type"] = task_type
        backend_name = self.config.default_backend
        reason = "default backend"
        model_records: List[dict] = []

        if task.selected_backend:
            backend_name = task.selected_backend
            reason = "task override"
            if task.model:
                model_records = self._model_records_for_backend(task.model, backend_name)
                reason = "task override + model assignment"
        elif task.model:
            backend_name, reason, model_records = self._route_from_task_model(task)
        elif routing_mode == "manual" and self.config.routing.manual_backend:
            backend_name = self.config.routing.manual_backend
            reason = "manual override"
        elif routing_mode == "rules":
            backend_name, reason = self._rules_based(task)
        elif routing_mode == "auto":
            backend_name, reason, model_records = self._auto_profile_routing(task)

        if backend_name == "aider_cli" and not model_records:
            model_records = select_openrouter_model(task)
            metadata["openrouter_models"] = model_records

        model_names = [record["name"] for record in model_records]
        model_tags = {record["name"]: record["tags"] for record in model_records}
        metadata["reason"] = reason
        metadata["plan_phase"] = task.phase
        if task.model:
            metadata["task_model"] = task.model
        return RoutingDecision(
            backend_name=backend_name,
            reason=reason,
            metadata=metadata,
            models=model_names,
            model_tags=model_tags,
            task_type=task_type,
        )

    def _rules_based(self, task: TaskDocument) -> tuple[str, str]:
        if "refactor" in task.title.lower():
            return "aider_cli", "rules: refactor tasks prefer aider"
        if task.phase.lower().startswith("research"):
            return "claude_code_cli", "rules: research phase"
        return self.config.default_backend, "rules: fallback default"

    def _auto_placeholder(self, task: TaskDocument) -> tuple[str, str]:
        priority = len(task.acceptance_criteria)
        if priority > 2:
            return "codex_cli", "auto: complex task"
        return "gemini_cli", "auto: lightweight task"

    def _auto_profile_routing(self, task: TaskDocument) -> tuple[str, str, List[dict]]:
        from backends.openrouter_models import get_preferred_models

        preferred = get_preferred_models()
        if preferred:
            model_map = {model["name"]: model for model in OPENROUTER_MODELS}
            preferred_model = next((name for name in preferred if name in model_map), None)
            if preferred_model:
                return "aider_cli", "auto: preferred openrouter model", [model_map[preferred_model]]

        task_type = _infer_task_type(task)
        complexity = _infer_task_complexity(task)
        cost_tier = {"low": "low", "medium": "medium", "high": "high"}[complexity]
        context_size = {"low": 8000, "medium": 32000, "high": 64000}[complexity]

        selected_model = self.model_profiles.get_best_model(task_type, cost_tier, context_size)
        if not selected_model:
            backend_name, reason = self._auto_placeholder(task)
            return backend_name, reason, []

        if selected_model.startswith("openrouter/"):
            model_map = {model["name"]: model for model in OPENROUTER_MODELS}
            record = model_map.get(selected_model, {"name": selected_model, "tags": [], "context": context_size})
            return "aider_cli", f"auto: profile-selected model ({selected_model})", [record]
        if selected_model == "codex":
            return "codex_cli", "auto: profile-selected model (codex)", []
        if selected_model == "gemini":
            return "gemini_cli", "auto: profile-selected model (gemini)", []
        if selected_model == "claude-code":
            return "claude_code_cli", "auto: profile-selected model (claude-code)", []
        if selected_model == "aider":
            return "aider_cli", "auto: profile-selected model (aider)", []

        backend_name, reason = self._auto_placeholder(task)
        return backend_name, reason, []

    def _route_from_task_model(self, task: TaskDocument) -> tuple[str, str, List[dict]]:
        model_name = str(task.model)
        if model_name.startswith("openrouter/"):
            return "aider_cli", f"task model override ({model_name})", [_record_for_model(model_name)]
        if model_name == "codex":
            return "codex_cli", "task model override (codex)", [_record_for_model(model_name)]
        if model_name == "gemini":
            return "gemini_cli", "task model override (gemini)", [_record_for_model(model_name)]
        if model_name == "claude-code":
            return "claude_code_cli", "task model override (claude-code)", [_record_for_model(model_name)]
        if model_name == "aider":
            return "aider_cli", "task model override (aider)", [_record_for_model(model_name)]
        return self.config.default_backend, f"task model unrecognized ({model_name})", []

    def _model_records_for_backend(self, model_name: str, backend_name: str) -> List[dict]:
        if backend_name == "aider_cli" and (model_name == "aider" or model_name.startswith("openrouter/")):
            return [_record_for_model(model_name)]
        if backend_name == "codex_cli" and model_name == "codex":
            return [_record_for_model(model_name)]
        if backend_name == "gemini_cli" and model_name == "gemini":
            return [_record_for_model(model_name)]
        if backend_name == "claude_code_cli" and model_name == "claude-code":
            return [_record_for_model(model_name)]
        return []
