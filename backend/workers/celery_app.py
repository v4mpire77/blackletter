from celery import Celery

from ..core.config import settings

celery_app = Celery(
    "blackletter_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["backend.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=86400,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_pool_limit=10,
    task_routes={
        "backend.workers.tasks.process_contract": {"queue": "contract_processing"}
    },
)
