"""Planning models covering plans, phases, and tasks."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from models.project import TaskDocument


class PlanTask(BaseModel):
    """Representation of a plan task before execution."""

    task: TaskDocument
    dependencies: List[str] = Field(default_factory=list)
    status: str = "planned"


class PlanPhase(BaseModel):
    """One phase within a plan."""

    name: str
    objective: str
    status: str = "planned"
    tasks: List[PlanTask] = Field(default_factory=list)
    completed: bool = False
    completed_at: Optional[datetime] = None
    human_checkpoint: Optional[bool] = None


class PlanRecord(BaseModel):
    plan_version: str
    completed_phases: List[PlanPhase] = Field(default_factory=list)
    remaining_phases: List[PlanPhase] = Field(default_factory=list)


class Plan(BaseModel):
    """Top-level project plan."""

    project_name: str
    summary: str
    phases: List[PlanPhase]
    version: str = "v1"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def record_completion(self, phase_name: str) -> None:
        for phase in self.phases:
            if phase.name == phase_name:
                phase.completed = True
                phase.status = "completed"
                phase.completed_at = datetime.utcnow()
