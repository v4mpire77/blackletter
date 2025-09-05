import os
import io

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
os.environ.setdefault("CELERY_BROKER_URL", "redis://localhost:6379/0")
os.environ.setdefault("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
os.environ.setdefault("SECRET_KEY", "test")

from fastapi.testclient import TestClient
from backend.main import app
from backend.workers import process_contract

client = TestClient(app)

PDF_BYTES = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"


def test_review_contract_creates_job_and_worker_completes():
    files = {"file": ("test.pdf", io.BytesIO(PDF_BYTES), "application/pdf")}
    r = client.post("/api/v1/jobs/", files=files)
    job_id = r.json()["job_id"]

    process_contract(job_id)

    status = client.get(f"/api/v1/jobs/{job_id}/status").json()
    assert status["status"] == "completed"
