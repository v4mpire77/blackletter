"""Review endpoints for processor obligation checks."""
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..models.schemas import ReviewResult

router = APIRouter()

@router.post("/review", response_model=ReviewResult, status_code=202)
async def create_review(file: UploadFile = File(...)) -> ReviewResult:
    """Enqueue a new contract review job. Stub implementation."""
    return ReviewResult(job_id="stub", status="queued", created_at="1970-01-01T00:00:00Z")

@router.get("/review/{job_id}", response_model=ReviewResult)
async def get_review(job_id: str) -> ReviewResult:
    """Fetch review status or result. Stub implementation."""
    if job_id != "stub":
        raise HTTPException(status_code=404, detail="job not found")
    return ReviewResult(job_id=job_id, status="completed", summary="stub", risk="low", issues=[], created_at="1970-01-01T00:00:00Z")

@router.get("/review/{job_id}/report")
async def get_report(job_id: str) -> dict:
    """Return placeholder report URLs."""
    if job_id != "stub":
        raise HTTPException(status_code=404, detail="job not found")
    return {"html_url": "https://example.com/report.html", "pdf_url": "https://example.com/report.pdf"}

@router.delete("/review/{job_id}", status_code=204)
async def delete_review(job_id: str) -> None:
    """Delete review artifacts. Stub implementation."""
    if job_id != "stub":
        raise HTTPException(status_code=404, detail="job not found")
    return None
