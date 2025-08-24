from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone

router = APIRouter(prefix="/api", tags=["issues"])


class Issue(BaseModel):
    id: str
    docId: str
    docName: str
    clausePath: str
    type: str  # "GDPR" | "Statute" | "Case Law"
    citation: str
    severity: str  # "High" | "Medium" | "Low"
    confidence: float
    status: str  # "Open" | "In Review" | "Resolved"
    owner: Optional[str] = None
    snippet: str
    recommendation: str
    createdAt: str  # ISO


_ISSUES: List[Issue] = [
    Issue(
        id="ISS-1001",
        docId="DOC-ACME-MSA",
        docName="ACME × Blackletter — MSA (v3)",
        clausePath="5.2 → Data Protection → International Transfers",
        type="GDPR",
        citation="UK GDPR Art. 44–49; DPA 2018 Part 2",
        severity="High",
        confidence=0.91,
        status="Open",
        snippet="Supplier may transfer Customer Personal Data outside the UK without additional safeguards.",
        recommendation="Add IDTA/SCCs + Transfer Risk Assessment.",
        createdAt=datetime.now(timezone.utc).isoformat(),
    )
]


@router.get("/issues", response_model=List[Issue])
async def list_issues() -> List[Issue]:
    return list(reversed(_ISSUES))


@router.post("/analyze", response_model=Issue)
async def analyze(
    file: UploadFile | None = File(None),
    doc_id: str | None = Form(None),
    doc_name: str | None = Form(None),
) -> Issue:
    now = datetime.now(timezone.utc).isoformat()
    new_issue = Issue(
        id=f"ISS-{1000 + len(_ISSUES)}",
        docId=doc_id or "DOC-UPLOAD",
        docName=doc_name or (file.filename if file else "Uploaded Document"),
        clausePath="9.2 → Security → Breach Notification",
        type="GDPR",
        citation="UK GDPR Art. 33–34",
        severity="Medium",
        confidence=0.79,
        status="Open",
        snippet="Notify without undue delay within a 'reasonable time'.",
        recommendation="Replace with “within 24 hours of becoming aware” and include Art. 33(3) details.",
        createdAt=now,
    )
    _ISSUES.append(new_issue)
    return new_issue


@router.get("/gdpr-coverage")
async def gdpr_coverage(docId: str):
    return {
        "docId": docId,
        "items": [
            {"article": "Art. 28 — Processor", "status": "GAP"},
            {"article": "Arts. 44–49 — Transfers", "status": "GAP"},
            {"article": "Art. 32 — Security", "status": "OK"},
        ],
    }


@router.get("/statute-coverage")
async def statute_coverage(docId: str):
    return {
        "docId": docId,
        "items": [
            {"ref": "DPA 2018 Part 2", "status": "Partial"},
            {"ref": "PECR 2003", "status": "OK"},
        ],
    }


@router.get("/caselaw")
async def caselaw(docId: str):
    return {
        "docId": docId,
        "signals": [
            {"case": "Barclays v Various Claimants [2020] UKSC 13", "weight": 0.8},
            {"case": "Lloyd v Google [2021] UKSC 50", "weight": 0.7},
        ],
    }

