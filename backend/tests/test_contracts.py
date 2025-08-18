import asyncio
import types
import sys
from pathlib import Path
from io import BytesIO

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi import UploadFile
from routers import contracts


def test_review_contract_handles_page_without_text(monkeypatch):
    class DummyPage:
        def extract_text(self):
            return None

    class DummyPdf:
        pages = [DummyPage()]

    def fake_pdf_reader(_):
        return DummyPdf()

    monkeypatch.setattr(contracts, "PdfReader", fake_pdf_reader)

    class DummyResponse:
        choices = [types.SimpleNamespace(message=types.SimpleNamespace(content="Summary\n\n- Risk 1"))]

    class DummyCompletions:
        @staticmethod
        def create(*args, **kwargs):
            return DummyResponse()

    class DummyChat:
        completions = DummyCompletions()

    dummy_openai = types.SimpleNamespace(chat=DummyChat())
    monkeypatch.setattr(contracts, "openai", dummy_openai)

    upload = UploadFile(filename="test.pdf", file=BytesIO(b"%PDF"), headers={"content-type": "application/pdf"})
    result = asyncio.run(contracts.review_contract(upload))
    assert result.summary == "Summary"
    assert result.risks == ["Risk 1"]
