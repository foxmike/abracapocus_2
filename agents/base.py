"""Base agent definitions."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable

from runtime.deep_agent_factory import DeepAgentFactory


class BaseAgent:
    """Base wrapper around a Deep Agent."""

    def __init__(
        self,
        name: str,
        prompt_file: str,
        skills: Iterable[str],
        factory: DeepAgentFactory,
    ) -> None:
        self.name = name
        self.prompt_file = Path(prompt_file)
        self.skills = list(skills)
        self.runner = factory.create(name, self.prompt_file, self.skills)

    def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if hasattr(self.runner, "invoke"):
            return self.runner.invoke(payload)
        if callable(self.runner):  # pragma: no cover
            return self.runner(payload)
        raise RuntimeError(f"Unsupported runner for {self.name}")
