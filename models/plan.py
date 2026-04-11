"""Planning models covering plans, phases, and tasks."""
from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from models.project import TaskDocument


class PlanTask(BaseModel):
    """Representation of a plan task before execution."""

    task: TaskDocument
    dependencies: List[str] = Field(default_factory=list)


class PlanPhase(BaseModel):
    """One phase within a plan."""

    name: str
    objective: str
    status: str = "planned"
    tasks: List[PlanTask] = Field(default_factory=list)


class Plan(BaseModel):
    """Top-level project plan."""

    project_name: str
    summary: str
    phases: List[PlanPhase]
    version: str = "v1"
    created_at: datetime = Field(default_factory=datetime.utcnow)
