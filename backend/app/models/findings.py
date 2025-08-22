from typing import List, Literal
from pydantic import BaseModel
from .rules import Severity, Citation  # reuse if you split models

Verdict = Literal["compliant", "non_compliant", "weak", "insufficient_context"]

class Quote(BaseModel):
    text: str
    citation: Citation

class Finding(BaseModel):
    rule_id: str
    severity: Severity
    verdict: Verdict
    risk: Literal["low", "medium", "high"]
    rationale: str
    snippet: str
    improvements: List[str] = []
    quotes: List[Quote] = []
