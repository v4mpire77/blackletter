"""Database models and helpers for job tracking."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession

from .db.session import Base, engine


class Job(Base):
    """SQLAlchemy model representing a contract review job."""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    contract_type = Column(String, nullable=False)
    jurisdiction = Column(String, nullable=True)
    status = Column(String, default="queued")
    created_at = Column(DateTime, default=datetime.utcnow)


async def create_job_record(
    session: AsyncSession, file_path: str, contract_type: str, jurisdiction: str
) -> int:
    """Persist a new job to the database and return its ID."""

    job = Job(
        file_path=file_path,
        contract_type=contract_type,
        jurisdiction=jurisdiction,
        status="queued",
    )
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job.id


async def get_job(session: AsyncSession, job_id: int) -> Optional[Job]:
    """Retrieve a job by ID."""

    return await session.get(Job, job_id)


async def update_job_status(session: AsyncSession, job_id: int, status: str) -> None:
    """Update the status of a job."""

    job = await session.get(Job, job_id)
    if job is None:
        return
    job.status = status
    await session.commit()


async def _init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(_init_models())
