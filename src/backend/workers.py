"""Background task workers."""

from __future__ import annotations

import asyncio

from .database import update_job_status
from .db.session import AsyncSessionLocal


async def _process(job_id: int) -> None:
    await asyncio.sleep(0.1)
    async with AsyncSessionLocal() as session:
        await update_job_status(session, job_id, "completed")


def process_contract(job_id: int) -> None:
    """Placeholder background task that marks the job as complete."""

    asyncio.run(_process(job_id))
