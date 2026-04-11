"""Application configuration management."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from pydantic import BaseModel, Field

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


class VerificationCheckSettings(BaseModel):
    """Single deterministic verification command."""

    name: str
    command: List[str]
    description: str = ""


class VerificationProfileSettings(BaseModel):
    """Collection of verification checks grouped into a profile."""

    name: str
    checks: List[VerificationCheckSettings]


class VerificationSettings(BaseModel):
    """Verification configuration loaded from config/env."""

    active_profile: str = "default"
    profiles: Dict[str, VerificationProfileSettings] = Field(default_factory=dict)
    workdir: Path = Path(".")

    def active_checks(self, profile_name: str | None = None) -> List[VerificationCheckSettings]:
        profile_id = profile_name or self.active_profile
        profile = self.profiles.get(profile_id)
        if profile is None:
            raise ValueError(f"Unknown verification profile '{profile_id}'")
        return profile.checks

    def has_profile(self, profile_name: str) -> bool:
        return profile_name in self.profiles


@dataclass(slots=True)
class AppConfig:
    """Bundled configuration object shared across the system."""

    project_name: str
    environment: str
    deep_agent: DeepAgentSettings
    routing: RoutingSettings
    paths: PathSettings
    extra: Dict[str, Any]
    verification: VerificationSettings

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
    minimal_profile = VerificationProfileSettings(
        name="minimal",
        checks=[
            VerificationCheckSettings(
                name="py_compile",
                command=["python", "-m", "py_compile", "main.py"],
                description="Ensure main.py compiles",
            )
        ],
    )
    default_profile = VerificationProfileSettings(
        name="default",
        checks=[
            VerificationCheckSettings(
                name="py_compile",
                command=["python", "-m", "py_compile", "main.py"],
                description="Ensure main.py compiles",
            ),
            VerificationCheckSettings(
                name="demo_selfcheck",
                command=["python", "scripts/selfcheck.py"],
                description="Validate demo self-improvement log",
            ),
        ],
    )
    strict_profile = VerificationProfileSettings(
        name="strict",
        checks=[
            VerificationCheckSettings(
                name="py_compile",
                command=["python", "-m", "py_compile", "main.py"],
                description="Ensure main.py compiles",
            ),
            VerificationCheckSettings(
                name="pytest",
                command=["pytest", "-q"],
                description="Run project tests quietly",
            ),
            VerificationCheckSettings(
                name="pytest-strict",
                command=["pytest", "-q", "--maxfail=1"],
                description="Fail fast on the first issue",
            ),
        ],
    )
    profiles = {
        "minimal": minimal_profile,
        "default": default_profile,
        "strict": strict_profile,
    }
    active_profile_name = os.getenv("VERIFICATION_PROFILE", "default")
    if active_profile_name not in profiles:
        active_profile_name = "default"
    verification = VerificationSettings(
        active_profile=active_profile_name,
        profiles=profiles,
        workdir=paths.root_dir,
    )

    config = AppConfig(
        project_name=project_name,
        environment=environment,
        deep_agent=deep_agent,
        routing=routing,
        paths=paths,
        extra={},
        verification=verification,
    )
    return config
