if __package__ is None or __package__ == "":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from backend.services import llm  # type: ignore
else:
    from ..services import llm

class DummyClient:
    def generate(self, prompt, system=None, max_tokens=800):
        return "hi"

def test_generate_text(monkeypatch):
    monkeypatch.setenv("PROVIDER_ORDER", "gemini")
    monkeypatch.setattr(llm, "_client_for", lambda provider, models: DummyClient())
    result = llm.generate_text("hello")
    assert result == "hi"
