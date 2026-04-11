"""Application configuration management."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class DeepAgentSettings(BaseModel):
    """Parameters for LangChain Deep Agents."""

    model: str = "gpt-4o-mini"
    temperature: float = 0.1
    mock_mode: bool = True
    timeout_seconds: int = 60


class RoutingSettings(BaseModel):
    """Routing and backend behavior configuration."""

    default_backend: str = "codex_cli"
    manual_backend: str | None = None
    routing_mode: str = "manual"
    verification_required: bool = True
    reviewer_required: bool = True


class PathSettings(BaseModel):
    """Important filesystem paths."""

    root_dir: Path = Path(__file__).parent
    logs_dir: Path = Path("logs")
    reports_dir: Path = Path("reports")
    state_file: Path = Path("state/runtime_state.json")
    plans_dir: Path = Path("plans")
    tasks_dir: Path = Path("tasks")
    phases_dir: Path = Path("phases")


@dataclass(slots=True)
class AppConfig:
    """Bundled configuration object shared across the system."""

    project_name: str
    environment: str
    deep_agent: DeepAgentSettings
    routing: RoutingSettings
    paths: PathSettings
    extra: Dict[str, Any]

    @property
    def default_backend(self) -> str:
        return self.routing.manual_backend or self.routing.default_backend


def load_config() -> AppConfig:
    """Load config from environment + defaults."""

    paths = PathSettings()
    for directory in (
        paths.logs_dir,
        paths.reports_dir,
        paths.plans_dir,
        paths.tasks_dir,
        paths.phases_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    state_file = paths.state_file
    state_file.parent.mkdir(parents=True, exist_ok=True)
    if not state_file.exists():
        state_file.write_text("{}\n", encoding="utf-8")

    project_name = os.getenv("PROJECT_NAME", "abracapocus_2")
    environment = os.getenv("APP_ENV", "development")

    deep_agent = DeepAgentSettings(
        model=os.getenv("DEEP_AGENT_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("DEEP_AGENT_TEMPERATURE", "0.1")),
        mock_mode=os.getenv("DEEP_AGENT_MOCK_MODE", "true").lower() == "true",
        timeout_seconds=int(os.getenv("DEEP_AGENT_TIMEOUT_SECONDS", "60")),
    )
    routing = RoutingSettings(
        default_backend=os.getenv("DEFAULT_BACKEND", "codex_cli"),
        manual_backend=os.getenv("BACKEND_OVERRIDE") or None,
        routing_mode=os.getenv("ROUTING_MODE", "manual"),
        verification_required=os.getenv("REQUIRE_VERIFICATION", "true").lower() == "true",
        reviewer_required=os.getenv("REQUIRE_REVIEWER", "true").lower() == "true",
    )

    config = AppConfig(
        project_name=project_name,
        environment=environment,
        deep_agent=deep_agent,
        routing=routing,
        paths=paths,
        extra={},
    )
    return config
