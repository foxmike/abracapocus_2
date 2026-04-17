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
    working_directory: Optional[str] = None
    changed_files: List[dict] = Field(default_factory=list)
    diff_summary: str = ""
    model_attempts: List[str] = Field(default_factory=list)


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
    command: List[str] = Field(default_factory=list)
    exit_code: Optional[int] = None


class VerificationReport(BaseModel):
    status: str
    checks: List[VerificationCheck] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    notes: str = ""
    profile: str = "default"


class ChangeAssessment(BaseModel):
    task_intent: str
    changed_files_summary: str
    verification_summary: str
    assessment_status: str
    notes: str = ""


class OrchestrationReport(BaseModel):
    """Aggregate output saved under reports/."""

    plan_summary: str
    backend_executions: List[BackendExecution]
    review: ReviewReport
    verification: VerificationReport
    change_assessment: ChangeAssessment
    metadata: dict = Field(default_factory=dict)

    @property
    def backend_execution(self) -> BackendExecution:
        """Backwards-compatible accessor for the first backend execution."""

        return self.backend_executions[0]
