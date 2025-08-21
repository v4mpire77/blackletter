from __future__ import annotations
import io, re, datetime as dt
from typing import List, Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pypdf import PdfReader

from ..models.schemas import ReviewResult, Issue
from ..services.llm import generate_text

router = APIRouter()

MAX_CHARS = 6000

def _pdf_to_text(file_bytes: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        pages = []
        for p in reader.pages:
            pages.append(p.extract_text() or "")
        return "\n".join(pages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF parse failed: {e}")

def _heuristics(text: str, doc_name: str, doc_id: str) -> List[Issue]:
    issues: List[Issue] = []
    now = dt.datetime.utcnow().isoformat() + "Z"

    def add_issue(clause_path, type_, citation, severity, snippet, recommendation, conf):
        issues.append(Issue(
            id=f"ISS-{abs(hash(clause_path+citation))%100000}",
            docId=doc_id, docName=doc_name, clausePath=clause_path,
            type=type_, citation=citation, severity=severity,
            confidence=conf, status="Open", snippet=snippet[:400],
            recommendation=recommendation, createdAt=now
        ))

    lowtxt = text.lower()

    # International transfers / SCC/IDTA
    if re.search(r"transfer(s)?\s+outside\s+(the\s+)?(uk|europe|eea)", lowtxt):
        add_issue(
            "5.2 → Data Protection → International Transfers",
            "GDPR",
            "UK GDPR Arts. 44–49; DPA 2018 Part 2",
            "High",
            "Clause indicates transfers outside the UK/EEA without clear safeguards.",
            "Add safeguards (UK IDTA/Addendum or SCCs) and a documented Transfer Risk Assessment.",
            0.85
        )

    # Subprocessors authorisation
    if re.search(r"sub[-\s]?processor|subprocessor", lowtxt) and re.search(r"without\s+(prior|written)\s+authori[sz]ation", lowtxt):
        add_issue(
            "5.5 → Data Protection → Subprocessors",
            "GDPR",
            "UK GDPR Art. 28(2)-(4)",
            "Medium",
            "Subprocessors permitted without prior written authorisation.",
            "Use prior written authorisation or, at minimum, publish list + notice + right to object.",
            0.8
        )

    # Breach notification timing vagueness
    if re.search(r"personal\s+data\s+breach|security\s+incident", lowtxt) and re.search(r"without\s+undue\s+delay|reasonable\s+time", lowtxt):
        add_issue(
            "9.2 → Security → Breach Notification",
            "GDPR",
            "UK GDPR Arts. 33–34",
            "Medium",
            "Breach notification timing is vague.",
            "Specify: 'within 24 hours of becoming aware' for processors; include required details (Art. 33(3)).",
            0.78
        )

    # Liability blanket exclusions
    if re.search(r"exclude\s+all\s+liability|no\s+liability\s+for\s+any", lowtxt):
        add_issue(
            "2.3 → Liability → Carve-outs",
            "Case Law",
            "Barclays v Various Claimants [2020] UKSC 13; CRA 2015 context",
            "Low",
            "Overbroad liability exclusions may be unenforceable.",
            "Add carve‑outs for statutory duties, fraud, wilful misconduct, and non‑excludable liabilities.",
            0.7
        )

    return issues

@router.post("/review", response_model=ReviewResult)
async def review_contract(
    file: UploadFile = File(...),
    doc_type: str = Form("Lease"),
    jurisdiction: str = Form("UK"),
    doc_name: str = Form("Uploaded Contract"),
):
    if file.content_type not in ("application/pdf", "pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    raw = await file.read()
    text = _pdf_to_text(raw)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text extracted from PDF")
    text = text[:MAX_CHARS]

    system = "You are a UK legal compliance assistant. Be precise and concise. Cite UK GDPR/DPA when relevant."
    prompt = (
        f"Document type: {doc_type}\nJurisdiction: {jurisdiction}\n"
        f"Summarise key compliance risks in 4–6 bullet points based on the following excerpt:\n\n{text}"
    )
    summary = generate_text(prompt, system=system, max_tokens=500)

    issues = _heuristics(text, doc_name, doc_id="DOC-UPLOAD")
    return ReviewResult(
        summary=summary,
        risks=[i.citation for i in issues],
        redlines={},
        next_actions=["Review suggested redlines; add firm playbook for scoring."],
        issues=issues,
    )

# Text-based analyze endpoint (lets the UI call without file upload)
from pydantic import BaseModel
class AnalyzeRequest(BaseModel):
    text: str
    docName: str = "Pasted Text"
    jurisdiction: str = "UK"
    docType: str = "Contract"

@router.post("/analyze", response_model=ReviewResult)
def analyze_text(req: AnalyzeRequest):
    text = (req.text or "")[:MAX_CHARS]
    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty text")
    system = "You are a UK legal compliance assistant. Be precise and concise."
    summary = generate_text(
        f"Summarise key compliance risks (4–6 bullets) for a {req.docType} in {req.jurisdiction}:\n\n{text}",
        system=system,
        max_tokens=500,
    )
    issues = _heuristics(text, req.docName, doc_id="DOC-TEXT")
    return ReviewResult(summary=summary, issues=issues)
