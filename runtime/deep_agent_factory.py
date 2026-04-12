"""LangChain Deep Agents loader with local fallback."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable

from config import DeepAgentSettings

try:  # pragma: no cover - import guarded for optional dependency
    from deepagents import create_deep_agent as _create_deep_agent

    DEEPAGENTS_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised when dependency missing
    DEEPAGENTS_AVAILABLE = False
    _create_deep_agent = None


@dataclass
class LocalDeepAgent:
    """Deterministic fallback agent used when LangChain is unavailable."""

    name: str
    instructions: str
    skills: Iterable[str]

    def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        summary = payload.get("summary") or payload.get("goal") or "task"
        notes = f"{self.name} processed payload keys: {', '.join(sorted(payload))}"
        return {
            "agent": self.name,
            "summary": summary,
            "notes": notes,
            "instructions_excerpt": self.instructions.strip().splitlines()[:2],
            "skills": list(self.skills),
            "payload": payload,
        }


class DeepAgentFactory:
    """Factory that builds Deep Agents or deterministic local runners."""

    def __init__(self, settings: DeepAgentSettings):
        self.settings = settings

    def create(self, name: str, instructions_path: Path, skills: Iterable[str]):
        instructions = Path(instructions_path).read_text(encoding="utf-8")
        if self.settings.mock_mode or not DEEPAGENTS_AVAILABLE or _create_deep_agent is None:
            return LocalDeepAgent(name=name, instructions=instructions, skills=skills)
        return _create_deep_agent(
            model=self.settings.model,
            tools=[],
            system_prompt=instructions,
            skills=list(skills),
        )
