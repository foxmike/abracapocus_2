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
    """Parameters for LangChain Deep Agents (model format 'provider:model_name')."""

    model: str = "openai:gpt-4o"
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
    working_root: Path = Field(default_factory=Path.cwd)
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
class RetrySettings:
    """Bounded retry policy used by supervisor verification retries."""

    max_retries_tier_1: int = 2
    max_retries_tier_2: int = 1
    max_retries_tier_3: int = 1
    retry_delay_seconds: int = 2


@dataclass(slots=True)
class PaceSettings:
    min_seconds_between_calls: float = 0.0
    max_calls_per_minute: int = 0


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
    retry: RetrySettings
    pace: Dict[str, PaceSettings]

    @property
    def default_backend(self) -> str:
        return self.routing.manual_backend or self.routing.default_backend

    @property
    def max_retries_tier_1(self) -> int:
        return self.retry.max_retries_tier_1

    @max_retries_tier_1.setter
    def max_retries_tier_1(self, value: int) -> None:
        self.retry.max_retries_tier_1 = value

    @property
    def max_retries_tier_2(self) -> int:
        return self.retry.max_retries_tier_2

    @max_retries_tier_2.setter
    def max_retries_tier_2(self, value: int) -> None:
        self.retry.max_retries_tier_2 = value

    @property
    def max_retries_tier_3(self) -> int:
        return self.retry.max_retries_tier_3

    @max_retries_tier_3.setter
    def max_retries_tier_3(self, value: int) -> None:
        self.retry.max_retries_tier_3 = value


def load_config() -> AppConfig:
    """Load config from environment + defaults."""

    working_root_env = os.getenv("ABRACAPOCUS_WORKING_ROOT")
    paths = PathSettings(
        working_root=Path(working_root_env) if working_root_env else Path.cwd(),
    )
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
        model=os.getenv("DEEP_AGENT_MODEL", "openai:gpt-4o"),
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
    retry = RetrySettings(
        max_retries_tier_1=int(os.getenv("RETRY_TIER_1", "2")),
        max_retries_tier_2=int(os.getenv("RETRY_TIER_2", "1")),
        max_retries_tier_3=int(os.getenv("RETRY_TIER_3", "1")),
        retry_delay_seconds=int(os.getenv("RETRY_DELAY_SECONDS", "2")),
    )
    pace = {
        "aider_cli": PaceSettings(
            min_seconds_between_calls=float(os.getenv("AIDER_MIN_DELAY", "0")),
            max_calls_per_minute=int(os.getenv("AIDER_MAX_CALLS_PER_MINUTE", "0")),
        ),
        "gemini_cli": PaceSettings(
            min_seconds_between_calls=float(os.getenv("GEMINI_MIN_DELAY", "0")),
            max_calls_per_minute=int(os.getenv("GEMINI_MAX_CALLS_PER_MINUTE", "0")),
        ),
        "codex_cli": PaceSettings(
            min_seconds_between_calls=float(os.getenv("CODEX_MIN_DELAY", "0")),
            max_calls_per_minute=int(os.getenv("CODEX_MAX_CALLS_PER_MINUTE", "0")),
        ),
        "claude_code_cli": PaceSettings(
            min_seconds_between_calls=float(os.getenv("CLAUDE_MIN_DELAY", "0")),
            max_calls_per_minute=int(os.getenv("CLAUDE_MAX_CALLS_PER_MINUTE", "0")),
        ),
    }

    config = AppConfig(
        project_name=project_name,
        environment=environment,
        deep_agent=deep_agent,
        routing=routing,
        paths=paths,
        extra={},
        verification=verification,
        retry=retry,
        pace=pace,
    )
    return config
