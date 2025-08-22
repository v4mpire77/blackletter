from typing import List, Optional, Literal
from pydantic import BaseModel
from enum import Enum

class IssueType(str, Enum):
    GDPR = "GDPR"
    STATUTE = "Statute"
    CASE_LAW = "Case Law"
    OTHER = "Other"

class Severity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    size: int
    upload_time: str

class AnalysisProgress(BaseModel):
    doc_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    progress: float  # 0.0 to 1.0
    message: Optional[str] = None

class ReviewResult(BaseModel):
    summary: str
    risks: List[str]

class Issue(BaseModel):
    id: str
    docId: str
    docName: str
    clausePath: str
    type: IssueType
    citation: str
    severity: Severity
    confidence: float
    status: Literal["Open", "In Review", "Resolved"]
    owner: Optional[str] = None
    snippet: str
    recommendation: str
    createdAt: str

class AnalysisResult(BaseModel):
    doc_id: str
    filename: str
    issues: List[Issue]
    summary: str
    risks: List[str]
    metadata: Optional[dict] = None
