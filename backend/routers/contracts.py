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
    """
    Accepts an uploaded contract (PDF or text).
    Extracts text, passes it to the LLMAdapter for summarisation + risk flags.
    Always returns a JSON ReviewResult with summary + risks.
    """
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    text = ""
    try:
        if file.filename and file.filename.lower().endswith(".pdf"):
            # Try reading first ~10 pages for performance
            reader = PdfReader(BytesIO(data))
            for page in reader.pages[:10]:
                text += page.extract_text() or ""
        else:
            # Treat as text input if not PDF
            text = data.decode(errors="ignore")
    except Exception as e:
        # Fallback: show first 1000 bytes as string
        text = data[:1000].decode(errors="ignore")
        if not text.strip():
            raise HTTPException(status_code=500, detail=f"Failed to extract text: {e}")

    if not text.strip():
        text = "No extractable text found."

    adapter = LLMAdapter()
    result = adapter.summarize(text)

    return ReviewResult(**result)
