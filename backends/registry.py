"""Backend registry and routing support."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List

from backends.aider_cli import AiderCliBackend
from backends.base import CodingBackend
from backends.claude_code_cli import ClaudeCodeCliBackend
from backends.codex_cli import CodexCliBackend
from backends.gemini_cli import GeminiCliBackend


@dataclass(slots=True)
class BackendDescriptor:
    name: str
    description: str
    factory: Callable[[], CodingBackend]


class BackendRegistry:
    """Registry for coding backends."""

    def __init__(self) -> None:
        self._registry: Dict[str, BackendDescriptor] = {
            "codex_cli": BackendDescriptor(
                name="codex_cli",
                description="Codex CLI coding agent",
                factory=lambda: CodexCliBackend(),
            ),
            "claude_code_cli": BackendDescriptor(
                name="claude_code_cli",
                description="Claude Code CLI coding agent",
                factory=lambda: ClaudeCodeCliBackend(),
            ),
            "gemini_cli": BackendDescriptor(
                name="gemini_cli",
                description="Gemini Code CLI coding agent",
                factory=lambda: GeminiCliBackend(),
            ),
            "aider_cli": BackendDescriptor(
                name="aider_cli",
                description="Aider CLI agent",
                factory=lambda: AiderCliBackend(),
            ),
        }

    def list_backends(self) -> List[BackendDescriptor]:
        return list(self._registry.values())

    def names(self) -> List[str]:
        return list(self._registry.keys())

    def get(self, name: str) -> CodingBackend:
        if name not in self._registry:
            raise KeyError(f"Unknown backend {name}")
        return self._registry[name].factory()

    def describe(self, name: str) -> BackendDescriptor:
        if name not in self._registry:
            raise KeyError(name)
        return self._registry[name]


REGISTRY = BackendRegistry()
