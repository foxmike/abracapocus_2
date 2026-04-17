"""Project and task request models."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProjectRequest(BaseModel):
    """Input provided to the supervisor."""

    project_name: str
    goal: str
    context: Optional[str] = None
    constraints: List[str] = Field(default_factory=list)


class TaskDocument(BaseModel):
    """Structured task used by coding backends."""

    task_id: str
    title: str
    description: str
    phase: str
    status: str = "pending"
    acceptance_criteria: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    selected_backend: Optional[str] = None
    model: Optional[str] = None
    verification_profile: Optional[str] = None


class ContextPackage(BaseModel):
    """Repo/doc context assembled by the research agent."""

    summaries: List[str]
    files: List[str]
    notes: str
    agents_md: str = ""
    agents_metadata: dict = Field(default_factory=dict)
