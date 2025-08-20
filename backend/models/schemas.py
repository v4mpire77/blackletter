from typing import List, Optional, Literal
from pydantic import BaseModel

class ReviewResult(BaseModel):
    summary: str
    risks: List[str]

class Issue(BaseModel):
    id: str
    docId: str
    docName: str
    clausePath: str
    type: Literal["GDPR", "Statute", "Case Law"]
    citation: str
    severity: Literal["High", "Medium", "Low"]
    confidence: float
    status: Literal["Open", "In Review", "Resolved"]
    owner: Optional[str] = None
    snippet: str
    recommendation: str
    createdAt: str
