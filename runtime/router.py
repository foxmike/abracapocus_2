"""Backend routing policies."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from backends.openrouter_models import OPENROUTER_MODELS
from backends.registry import REGISTRY
from config import AppConfig
from models.project import TaskDocument

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


def select_openrouter_model(task: TaskDocument) -> List[dict]:
    """Select the best OpenRouter models for the task."""

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


@dataclass(slots=True)
class RoutingDecision:
    backend_name: str
    reason: str
    metadata: Dict[str, Any]
    models: List[str] = field(default_factory=list)
    model_tags: Dict[str, List[str]] = field(default_factory=dict)
    task_type: str | None = None

    def backend(self):
        return REGISTRY.get(self.backend_name)


class BackendRouter:
    """Simple routing policy manager."""

    def __init__(self, config: AppConfig):
        self.config = config

    def select(self, task: TaskDocument) -> RoutingDecision:
        routing_mode = self.config.routing.routing_mode
        metadata: Dict[str, Any] = {"routing_mode": routing_mode}
        task_type = _infer_task_type(task)
        metadata["task_type"] = task_type
        backend_name = self.config.default_backend
        reason = "default backend"
        model_records: List[dict] = []

        if routing_mode == "manual" and self.config.routing.manual_backend:
            backend_name = self.config.routing.manual_backend
            reason = "manual override"
        elif routing_mode == "rules":
            backend_name, reason = self._rules_based(task)
        elif routing_mode == "auto":
            backend_name, reason = self._auto_placeholder(task)

        if backend_name == "aider_cli":
            model_records = select_openrouter_model(task)
            metadata["openrouter_models"] = model_records

        model_names = [record["name"] for record in model_records]
        model_tags = {record["name"]: record["tags"] for record in model_records}
        metadata["reason"] = reason
        metadata["plan_phase"] = task.phase
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
