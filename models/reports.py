"""Execution, review, and verification report models."""
from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class BackendExecution(BaseModel):
    backend: str
    command: List[str]
    stdout: str
    stderr: str
    exit_code: int
    duration_seconds: float


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
    backend_execution: BackendExecution
    review: ReviewReport
    verification: VerificationReport
    metadata: dict = Field(default_factory=dict)
