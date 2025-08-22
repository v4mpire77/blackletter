from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from enum import Enum
from datetime import datetime

# Type definitions
Severity = Literal["High", "Medium", "Low"]
IssueType = Literal["GDPR", "Statute", "Case Law", "Other"]
IssueStatus = Literal["Open", "In Review", "Resolved"]

# Legacy enum classes for backward compatibility
class SeverityEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium" 
    HIGH = "High"

class IssueTypeEnum(str, Enum):
    GDPR = "GDPR"
    STATUTE = "Statute"
    CASE_LAW = "Case Law"
    OTHER = "Other"

# Core data models
class Issue(BaseModel):
    id: str
    docId: str
    docName: str
    clausePath: str
    type: IssueType
    citation: str
    severity: Severity
    confidence: float = Field(ge=0, le=1)
    status: IssueStatus = "Open"
    owner: Optional[str] = None
    snippet: str
    recommendation: str
    createdAt: str

class UploadResponse(BaseModel):
    filename: str
    size: int
    doc_id: str
    upload_time: Optional[str] = None

class AnalysisResponse(BaseModel):
    filename: str
    size: int
    issues: List[Any] = []

class AnalysisResult(BaseModel):
    doc_id: str
    filename: str
    issues: List[Issue]
    summary: str
    risks: List[str]
    metadata: Optional[Dict[str, Any]] = None

class AnalysisProgress(BaseModel):
    doc_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    progress: float = Field(ge=0, le=1)
    message: Optional[str] = None

class ReviewResult(BaseModel):
    summary: str
    risks: List[str] = []
    redlines: Dict[str, Any] = {}
    next_actions: List[str] = []
    issues: List[Issue] = []

# --- Enhanced Data Models for Advanced Features ---

class RuleSeverity(str, Enum):
    red = "red"
    amber = "amber"
    green = "green"

class RuleSource(BaseModel):
    url: str
    version_label: str

class RuleLogic(BaseModel):
    contains_text: List[str] = []

class RuleDefinition(BaseModel):
    id: str
    domain: str
    title: str
    severity: RuleSeverity
    source: RuleSource
    logic: RuleLogic
    remedy: Optional[str] = None

class EvidenceItem(BaseModel):
    rule_id: str
    source_url: str
    source_version: str
    approver_id: Optional[str] = None
    timestamp: datetime
    hash: Optional[str] = None

class EvidenceBundle(BaseModel):
    items: List[EvidenceItem] = []

class FindingType(str, Enum):
    rule_violation = "rule_violation"
    vague_term = "vague_term"
    metadata = "metadata"

class Location(BaseModel):
    page: Optional[int] = None
    clause_path: Optional[str] = None

class Finding(BaseModel):
    id: str
    type: FindingType
    title: str
    description: str
    severity: Optional[RuleSeverity] = None
    location: Optional[Location] = None
    remediation: Optional[str] = None
    evidence: List[EvidenceItem] = []

class ContractMetadata(BaseModel):
    doc_id: str
    filename: str
    size: int
    uploaded_at: Optional[datetime] = None

class ContractAnalysis(BaseModel):
    metadata: ContractMetadata
    summary: Optional[str] = None
    findings: List[Finding] = []
    evidence_chain: EvidenceBundle = EvidenceBundle()
    risks: List[str] = []
    redlines: Dict[str, Any] = {}
    next_actions: List[str] = []
