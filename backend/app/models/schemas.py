"""Pydantic models for review results."""
from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

Severity = Literal["High", "Medium", "Low"]


class Issue(BaseModel):
    rule_id: str
    description: str
    compliant: bool
    severity: Severity
    details: Optional[str] = None
    citation: Optional[str] = None
    clausePath: Optional[str] = None
    recommendation: Optional[str] = None


class Metrics(BaseModel):
    precision: float = Field(ge=0, le=1)
    recall: float = Field(ge=0, le=1)
    latency_ms: int


class ReviewResult(BaseModel):
    job_id: str
    status: Literal["queued", "processing", "completed", "error"]
    summary: Optional[str] = None
    risk: Optional[Literal["low", "medium", "high"]] = None
    issues: List[Issue] = []
    metrics: Optional[Metrics] = None
    report: Optional[dict] = None
    created_at: datetime
