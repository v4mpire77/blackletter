import json
import os
import sys
from types import SimpleNamespace

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import rag


def test_refuses_on_low_score():
    ctx = [{"source_id": "A", "page": 1, "content": "text", "score": 0.1}]
    res = rag.generate_answer("question", ctx, threshold=0.5)
    assert "enough information" in res["answer"].lower()
    assert res["citations"] == []


def test_generate_answer_with_mock(monkeypatch):
    def fake_create(model, input):
        payload = {
            "answer": "Answer.",
            "citations": [
                {"source_id": "A", "page": 1, "quote": "foo"},
                {"source_id": "B", "page": 2, "quote": "bar"},
            ],
            "confidence": 0.8,
        }
        return SimpleNamespace(
            output=[
                SimpleNamespace(
                    content=[SimpleNamespace(text=json.dumps(payload))]
                )
            ]
        )

    class FakeClient:
        def __init__(self):
            self.responses = SimpleNamespace(create=fake_create)

    monkeypatch.setattr(rag, "OpenAI", lambda: FakeClient())

    contexts = [
        {"source_id": "A", "page": 1, "content": "foo", "score": 0.9},
        {"source_id": "B", "page": 2, "content": "bar", "score": 0.8},
    ]
    res = rag.generate_answer("question", contexts)
    assert res["answer"] == "Answer."
    assert len(res["citations"]) == 2
    assert res["confidence"] == 0.8
