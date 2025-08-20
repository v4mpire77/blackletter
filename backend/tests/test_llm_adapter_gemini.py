import asyncio
from backend.app.core.llm_adapter import LLMAdapter

class DummyResponse:
    def __init__(self, data):
        self._data = data
    def json(self):
        return self._data
    def raise_for_status(self):
        pass

class DummyClient:
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc, tb):
        pass
    async def post(self, url, json, headers, timeout):
        assert "gemini-2.0-flash" in url
        return DummyResponse({"candidates": [{"content": {"parts": [{"text": "hi"}]}}]})


def test_gemini_adapter(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "test")
    monkeypatch.setenv("DEFAULT_LLM", "gemini-2.0-flash")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr("httpx.AsyncClient", DummyClient)
    adapter = LLMAdapter()
    result = asyncio.run(adapter.analyze_contract("text"))
    assert result == "hi"
