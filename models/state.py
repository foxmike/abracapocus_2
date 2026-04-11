"""Runtime state models."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    planned = "planned"
    in_progress = "in_progress"
    blocked = "blocked"
    completed = "completed"


class TaskRecord(BaseModel):
    task_id: str
    title: str
    phase: str
    status: TaskStatus = TaskStatus.planned
    backend: str
    last_run: Optional[datetime] = None
    notes: str = ""


class ExecutionHistory(BaseModel):
    run_id: str
    task_id: str
    backend: str
    status: str
    reviewer_status: str
    verifier_status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class RuntimeState(BaseModel):
    project_name: str
    plan_version: str
    active_phase: str
    default_backend: str
    routing_mode: str
    tasks: List[TaskRecord] = Field(default_factory=list)
    history: List[ExecutionHistory] = Field(default_factory=list)
    operator_overrides: dict = Field(default_factory=dict)
    completed_phases: List[str] = Field(default_factory=list)
    remaining_phases: List[str] = Field(default_factory=list)


def bootstrap_state(project_name: str, backend: str, routing_mode: str) -> RuntimeState:
    return RuntimeState(
        project_name=project_name,
        plan_version="v1",
        active_phase="planning",
        default_backend=backend,
        routing_mode=routing_mode,
    )
