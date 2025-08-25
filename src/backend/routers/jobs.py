"""API endpoints for creating and tracking review jobs."""

from __future__ import annotations

import os
import uuid
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import magic

from ..models.schemas import JobCreationResponse, JobStatusResponse, JobState
from ..database import create_job_record, get_job
from ..workers import process_contract
from ..db.session import get_db
from ..core.config import settings

router = APIRouter()


@router.post(
    "/",
    response_model=JobCreationResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_job(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    contract_type: str = Form("vendor_dpa"),
    jurisdiction: str = Form("EU"),
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """Accept a contract for review and enqueue background processing."""

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    mime_type = magic.from_buffer(contents, mime=True)
    if mime_type not in settings.ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    tmp_dir = os.getenv("TMP_DIR", "/tmp")
    ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(tmp_dir, f"{uuid.uuid4().hex}{ext}")
    try:
        with open(file_path, "wb") as f:
            f.write(contents)
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {exc}")

    job_id = await create_job_record(db, file_path, contract_type, jurisdiction)
    background_tasks.add_task(process_contract, job_id)

    status_url = f"{settings.API_V1_STR}/jobs/{job_id}/status"
    headers = {"Location": status_url}
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"job_id": job_id, "status": JobState.QUEUED},
        headers=headers,
    )


@router.get("/{job_id}/status", response_model=JobStatusResponse)
async def job_status(job_id: int, db: AsyncSession = Depends(get_db)) -> JobStatusResponse:
    """Return the status of a processing job."""

    job = await get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(job_id=job.id, status=job.status)
