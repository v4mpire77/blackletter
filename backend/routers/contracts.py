from fastapi import APIRouter, UploadFile, HTTPException, File, Form
from pypdf import PdfReader
from io import BytesIO
import json
import asyncio
import uuid
from typing import Dict

from ..services.gemini_client import ask_gemini
from ..models.schemas import ReviewResult

router = APIRouter()


@router.post("/review", response_model=ReviewResult)
async def review_contract(
    file: UploadFile = File(...),
    doc_type: str = Form("Contract"),
    jurisdiction: str = Form("UK"),
):
    """Analyze a contract PDF using Google's Gemini model."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    try:
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")

        def _extract(data: bytes) -> str:
            pdf = PdfReader(BytesIO(data))
            text_parts = []
            for page in pdf.pages:
                t = page.extract_text() or ""
                text_parts.append(t)
            return "\n\n".join(text_parts).strip()

        text = await asyncio.to_thread(_extract, content)
        if not text:
            raise HTTPException(status_code=400, detail="No extractable text found in PDF")

        truncated = text[:6000] + ("..." if len(text) > 6000 else "")

        prompt = (
            f"Summarise and flag compliance risks for a {doc_type} contract in {jurisdiction}.\n"
            "Return ONLY valid JSON with keys: summary (string) and risks (array of strings).\n\n"
            f"Text: {truncated}"
        )

        resp_text = ask_gemini(prompt)

        summary = ""
        risks = []
        try:
            parsed = json.loads(resp_text)
            summary = parsed.get("summary") or ""
            risks = parsed.get("risks") or []
            if isinstance(risks, str):
                risks = [risks]
        except Exception:
            summary = resp_text.strip()

        if not risks:
            risks = ["No significant risks identified."]

        return ReviewResult(summary=summary, risks=risks)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")


# In-memory storage for uploaded contracts
contracts_store: Dict[str, ReviewResult] = {}


@router.post("/contracts")
async def create_contract(file: UploadFile):
    """Upload a contract and run checks."""
    result = await review_contract(file)
    contract_id = str(uuid.uuid4())
    contracts_store[contract_id] = result
    return {"id": contract_id}


@router.get("/contracts/{contract_id}/findings", response_model=ReviewResult)
async def get_contract_findings(contract_id: str):
    result = contracts_store.get(contract_id)
    if not result:
        raise HTTPException(status_code=404, detail="Contract not found")
    return result


@router.get("/contracts/{contract_id}/report")
async def get_contract_report(contract_id: str):
    result = contracts_store.get(contract_id)
    if not result:
        raise HTTPException(status_code=404, detail="Contract not found")
    lines = ["# Contract Report", "", "## Summary", result.summary, "", "## Key Risks"]
    lines.extend(f"- {r}" for r in result.risks)
    return {"report": "\n".join(lines)}
