"""Research agent for context gathering."""
from __future__ import annotations

from pathlib import Path
from typing import List

from agents.base import BaseAgent
from models.project import ContextPackage, ProjectRequest
from runtime.deep_agent_factory import DeepAgentFactory
from runtime.context_store import ContextStore


class ResearchAgent(BaseAgent):
    def __init__(self, factory: DeepAgentFactory, repo_root: Path | str | None = None) -> None:
        super().__init__(
            name="research_agent",
            prompt_file="prompts/research.md",
            skills=["skills/repo_inspection", "skills/documentation_generation"],
            factory=factory,
        )
        self.repo_root = Path(repo_root or ".").resolve()
        self.context_store = ContextStore()
        self._indexed = False

    def gather(self, request: ProjectRequest) -> ContextPackage:
        self._ensure_indexed()
        matches = self.context_store.query(request.goal, k=25)
        files = self._extract_files(matches)
        payload = {"goal": request.goal, "files": files}
        response = self.invoke(payload)
        summaries = [
            f"Project goal: {request.goal}",
            f"Files analyzed: {len(files)}",
        ]
        if isinstance(response, dict) and response.get("notes"):
            summaries.append(response["notes"])
        return ContextPackage(
            summaries=summaries,
            files=files,
            notes=f"Collected {len(files)} semantically relevant files",
        )

    def update_files(self, changed_files: list[dict] | list[str]) -> None:
        self._ensure_indexed()
        paths: List[str] = []
        for changed in changed_files:
            if isinstance(changed, dict):
                path = changed.get("path")
                if path:
                    paths.append(str(path))
                continue
            if changed:
                paths.append(str(changed))
        if not paths:
            return
        self.context_store.update_files(paths)

    def _ensure_indexed(self) -> None:
        if self._indexed:
            return
        self.context_store.index_repo(self.repo_root)
        self._indexed = True

    def _extract_files(self, matches: list[dict[str, object]]) -> list[str]:
        files: List[str] = []
        seen: set[str] = set()
        for match in matches:
            path = match.get("path")
            if not isinstance(path, str) or not path or path in seen:
                continue
            seen.add(path)
            files.append(path)
        return files
