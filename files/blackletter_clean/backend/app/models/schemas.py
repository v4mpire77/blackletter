from pydantic import BaseModel, Field, validator
from typing import List, Literal, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

# Enums for type safety
class JobStatusEnum(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class SeverityEnum(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class IssueTypeEnum(str, Enum):
    GDPR = "GDPR"
    STATUTE = "Statute"
    CASE_LAW = "Case Law"

class IssueStatusEnum(str, Enum):
    OPEN = "Open"
    IN_REVIEW = "In Review"
    RESOLVED = "Resolved"

class CoverageStatusEnum(str, Enum):
    OK = "OK"
    PARTIAL = "Partial"
    GAP = "GAP"

class Issue(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    doc_id: str
    clause_path: str
    type: IssueTypeEnum = Field(default=IssueTypeEnum.GDPR)
    citation: str
    severity: SeverityEnum
    confidence: float = Field(..., ge=0, le=1)
    status: IssueStatusEnum = Field(default=IssueStatusEnum.OPEN)
    snippet: str
    recommendation: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Confidence must be between 0 and 1')
        return round(v, 3)

class Coverage(BaseModel):
    article: str
    status: CoverageStatusEnum
    details: Optional[str] = None
    found_clauses: List[str] = Field(default_factory=list)

class JobStatus(BaseModel):
    id: str
    status: JobStatusEnum
    progress: Optional[int] = 0
    filename: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None

class JobResult(BaseModel):
    job_id: str
    issues: List[Issue]
    coverage: List[Coverage]
    summary: str
    confidence_score: float = Field(..., ge=0, le=1)
    processing_time_seconds: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class JobCreateResponse(BaseModel):
    job_id: str
    status: JobStatusEnum = JobStatusEnum.QUEUED
    message: str = "Job created successfully"