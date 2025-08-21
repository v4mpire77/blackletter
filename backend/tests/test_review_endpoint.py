from pathlib import Path
from fastapi.testclient import TestClient

if __package__ is None or __package__ == "":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from backend.main import app  # type: ignore
else:
    from ..main import app


def test_review_endpoint_returns_results(monkeypatch):
    monkeypatch.setattr("backend.routers.contracts.generate_text", lambda *args, **kwargs: "ok")
    client = TestClient(app)
    pdf_path = Path("backend/tests/fixtures/uk_nda.pdf")
    with pdf_path.open("rb") as f:
        files = {"file": ("uk_nda.pdf", f, "application/pdf")}
        resp = client.post("/api/review", files=files)
    assert resp.status_code == 200
    data = resp.json()
    assert data["summary"] == "ok"
    assert isinstance(data["issues"], list)
