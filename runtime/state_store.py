"""JSON-backed runtime state store."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict

from config import AppConfig
from models.state import RuntimeState, bootstrap_state


class StateStore:
    def __init__(self, config: AppConfig):
        self.config = config
        self.path = config.paths.state_file
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.write_state(bootstrap_state(config.project_name, config.default_backend, config.routing.routing_mode))

    def read_state(self) -> RuntimeState:
        raw = json.loads(self.path.read_text(encoding="utf-8") or "{}")
        if not raw:
            return bootstrap_state(
                self.config.project_name,
                self.config.default_backend,
                self.config.routing.routing_mode,
            )
        return RuntimeState(**raw)

    def write_state(self, state: RuntimeState) -> None:
        self.path.write_text(state.model_dump_json(indent=2), encoding="utf-8")

    def update(self, fn: Callable[[RuntimeState], RuntimeState]) -> RuntimeState:
        state = self.read_state()
        new_state = fn(state)
        self.write_state(new_state)
        return new_state

    def reset(self) -> RuntimeState:
        state = bootstrap_state(
            self.config.project_name,
            self.config.default_backend,
            self.config.routing.routing_mode,
        )
        self.write_state(state)
        return state
