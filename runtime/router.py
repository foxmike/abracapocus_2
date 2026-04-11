"""Backend routing policies."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from backends.registry import REGISTRY
from config import AppConfig
from models.project import TaskDocument


@dataclass(slots=True)
class RoutingDecision:
    backend_name: str
    reason: str
    metadata: Dict[str, str]

    def backend(self):
        return REGISTRY.get(self.backend_name)


class BackendRouter:
    """Simple routing policy manager."""

    def __init__(self, config: AppConfig):
        self.config = config

    def select(self, task: TaskDocument) -> RoutingDecision:
        routing_mode = self.config.routing.routing_mode
        metadata: Dict[str, str] = {"routing_mode": routing_mode}
        backend_name = self.config.default_backend
        reason = "default backend"

        if routing_mode == "manual" and self.config.routing.manual_backend:
            backend_name = self.config.routing.manual_backend
            reason = "manual override"
        elif routing_mode == "rules":
            backend_name, reason = self._rules_based(task)
        elif routing_mode == "auto":
            backend_name, reason = self._auto_placeholder(task)

        metadata["reason"] = reason
        metadata["plan_phase"] = task.phase
        return RoutingDecision(backend_name=backend_name, reason=reason, metadata=metadata)

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
