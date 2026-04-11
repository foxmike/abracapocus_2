"""LangChain Deep Agents loader with local fallback."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from config import DeepAgentSettings


def _try_import_create_deep_agent() -> Optional[Any]:
    """Attempt to import create_deep_agent from known locations."""

    candidates = (
        "langchain.agents.deep_agents.base",
        "langchain_deep_agents.factory",
        "langchain_experimental.deep_agents",
    )
    for module_name in candidates:
        try:
            module = __import__(module_name, fromlist=["create_deep_agent"])
            return getattr(module, "create_deep_agent")
        except (ImportError, AttributeError):
            continue
    return None


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
        self._create_deep_agent = None if settings.mock_mode else _try_import_create_deep_agent()
        self._llm = None
        if self._create_deep_agent is not None:
            self._llm = self._build_llm()

    def _build_llm(self) -> Optional[Any]:
        try:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=self.settings.model,
                temperature=self.settings.temperature,
                timeout=self.settings.timeout_seconds,
            )
        except ImportError:
            return None

    def create(self, name: str, instructions_path: Path, skills: Iterable[str]):
        instructions = Path(instructions_path).read_text(encoding="utf-8")
        if self._create_deep_agent is None or self._llm is None:
            return LocalDeepAgent(name=name, instructions=instructions, skills=skills)
        return self._create_deep_agent(
            name=name,
            llm=self._llm,
            instructions=instructions,
            skills=list(skills),
            max_iterations=4,
        )
