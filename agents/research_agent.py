"""Research agent for context gathering."""
from __future__ import annotations

from pathlib import Path
from typing import List

from agents.base import BaseAgent
from models.project import ContextPackage, ProjectRequest
from runtime.deep_agent_factory import DeepAgentFactory


class ResearchAgent(BaseAgent):
    def __init__(self, factory: DeepAgentFactory) -> None:
        super().__init__(
            name="research_agent",
            prompt_file="prompts/research.md",
            skills=["skills/repo_inspection", "skills/documentation_generation"],
            factory=factory,
        )

    def gather(self, request: ProjectRequest) -> ContextPackage:
        repo_summary = self._scan_repo()
        payload = {"goal": request.goal, "files": repo_summary["files"]}
        response = self.invoke(payload)
        summaries = [
            f"Project goal: {request.goal}",
            f"Files analyzed: {len(repo_summary['files'])}",
        ]
        if isinstance(response, dict) and response.get("notes"):
            summaries.append(response["notes"])
        return ContextPackage(
            summaries=summaries,
            files=repo_summary["files"],
            notes="; ".join(repo_summary["notes"]),
        )

    def _scan_repo(self) -> dict:
        include_suffixes = {".py", ".md", ".json"}
        files: List[str] = []
        notes: List[str] = []
        root = Path('.')
        for path in sorted(root.rglob('*')):
            if any(part.startswith('.git') for part in path.parts):
                continue
            if path.is_file() and path.suffix in include_suffixes and 'state' not in path.parts:
                files.append(str(path))
                if len(files) >= 25:
                    break
        notes.append(f"Collected {len(files)} documentation/code files")
        return {"files": files, "notes": notes}
