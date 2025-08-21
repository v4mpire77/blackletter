from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class IssueType(str, Enum):
    """Enum for different types of compliance issues."""
    DATA_PROTECTION = "data_protection"
    CONSUMER_RIGHTS = "consumer_rights"
    EMPLOYMENT = "employment"
    GDPR = "gdpr"
    IP_RIGHTS = "ip_rights"
    ANTI_MONEY_LAUNDERING = "anti_money_laundering"
    COMPETITION_LAW = "competition_law"
    ENVIRONMENTAL = "environmental"
    TAX = "tax"
    OTHER = "other"


class Severity(str, Enum):
    """Enum for issue severity levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Issue(BaseModel):
    """Model for a compliance issue detected in a contract."""
    id: str
    type: IssueType
    title: str
    description: str
    severity: Severity
    clause: Optional[str] = None
    page_number: Optional[int] = None
    remediation: Optional[str] = None
    timestamp: datetime


class UploadResponse(BaseModel):
    """Response model for file upload endpoint."""
    filename: str
    size: int
    doc_id: str


class AnalysisResponse(BaseModel):
    """Response model for contract analysis endpoint."""
    filename: str
    size: int
    issues: List[Issue]
