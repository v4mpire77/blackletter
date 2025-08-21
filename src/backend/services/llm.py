# Service wrapper around the Gemini-only LLMAdapter

from __future__ import annotations
from typing import Iterable, List, Optional

from backend.app.core.llm_adapter import LLMAdapter


class GeminiClient:
    """Minimal Gemini client used only for tests.

    The real implementation would call the external Gemini API.  Here we just
    provide the interface that tests expect and allow it to be easily mocked.
    """

    def generate(self, prompt: str, *, system: str | None = None, **_: object) -> str:
        return prompt

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(t))] for t in texts]

# Singleton-style adapter for simple apps; swap to DI if you prefer.
_llm: LLMAdapter | None = None


def get_llm() -> LLMAdapter:
    global _llm
    if _llm is None:
        _llm = LLMAdapter()
    return _llm


# --------- Convenience functions used by routes/services ---------

def generate_text(prompt: str, system: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 2048) -> str:
    llm = get_llm()
    return llm.generate(prompt=prompt, system=system, temperature=temperature, max_output_tokens=max_tokens)


def embed_texts(texts: Iterable[str]) -> List[List[float]]:
    llm = get_llm()
    return llm.embed_texts(list(texts))


def health() -> dict:
    return get_llm().health()
