"""Celery tasks for contract review."""
from celery import Celery

celery_app = Celery("blackletter")


@celery_app.task(name="contracts.review")
def run_review(job_id: str, playbook_id: str) -> str:
    """Background review pipeline. Stub implementation."""
    return job_id
