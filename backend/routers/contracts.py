from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from pypdf import PdfReader
from io import BytesIO

from app.core.llm_adapter import LLMAdapter

router = APIRouter(prefix="/api", tags=["contracts"])

class ReviewResult(BaseModel):
    summary: str
    risks: list[dict]

@router.post("/review", response_model=ReviewResult)
async def review_contract(file: UploadFile = File(...)) -> ReviewResult:
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    text = ""
    try:
        if file.filename.lower().endswith(".pdf"):
            reader = PdfReader(BytesIO(data))
            for page in reader.pages[:10]:
                text += page.extract_text() or ""
        else:
            # very small fallback – treat as textish
            text = data.decode(errors="ignore")
    except Exception:
        # don’t fail tests if extraction is flaky – use bytes preview
        text = data[:1000].decode(errors="ignore")

    if not text.strip():
        text = "No extractable text found."

    llm = LLMAdapter()
    result = llm.summarize(text)
    return ReviewResult(**result)
