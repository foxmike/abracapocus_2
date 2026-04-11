"""Execution, review, and verification report models."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BackendExecution(BaseModel):
    backend: str
    command: List[str]
    stdout: str
    stderr: str
    exit_code: int
    duration_seconds: float
    model: Optional[str] = None
    model_tags: List[str] = Field(default_factory=list)
    task_type: Optional[str] = None


class ReviewFinding(BaseModel):
    severity: str
    location: str
    detail: str


class ReviewReport(BaseModel):
    status: str
    findings: List[ReviewFinding] = Field(default_factory=list)
    summary: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VerificationCheck(BaseModel):
    name: str
    status: str
    detail: str


class VerificationReport(BaseModel):
    status: str
    checks: List[VerificationCheck] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    notes: str = ""


class OrchestrationReport(BaseModel):
    """Aggregate output saved under reports/."""

    plan_summary: str
    backend_executions: List[BackendExecution]
    review: ReviewReport
    verification: VerificationReport
    metadata: dict = Field(default_factory=dict)

    @property
    def backend_execution(self) -> BackendExecution:
        """Backwards-compatible accessor for the first backend execution."""

        return self.backend_executions[0]
