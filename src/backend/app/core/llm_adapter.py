import os
from typing import Any, Dict, Iterable, List


class LLMAdapter:
    """Lightweight adapter around different LLM providers.

    The real project uses Gemini/Ollama clients, but for the tests we keep the
    implementation deterministic and dependency‑free.  Only the pieces that the
    tests assert on are implemented.
    """

    def __init__(self) -> None:
        self.provider = (os.getenv("LLM_PROVIDER") or "gemini").lower()
        self.model = os.getenv("LLM_MODEL", "stub-model")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.ollama_reachable = False
        self.init_error: str | None = None

        if self.provider == "gemini" and not self.gemini_key:
            self.init_error = "GEMINI_API_KEY environment variable not set"
            raise RuntimeError(self.init_error)

    async def analyze_contract(self, text: str) -> Dict[str, Any]:
        """Asynchronously analyse a contract.

        In the stub implementation we simply call :meth:`summarize`.
        """
        return self.summarize(text)

    def summarize(self, text: str) -> Dict[str, Any]:
        """Return a deterministic structure the tests can assert on."""
        if self.provider == "stub":
            risks: List[str] = []
            lowered = text.lower()
            # very simple heuristics to always return something predictable
            if "data" in lowered or "personal" in lowered:
                risks.append("GDPR")
            if "liability" in lowered:
                risks.append("Liability")
            return {
                "summary": (text[:400] + "…") if len(text) > 400 else text,
                "risks": risks,
            }

        # Future: add gemini/openai branches guarded by API keys
        return {"summary": text[:400], "risks": []}

    # --- Convenience methods used by services.llm ---
    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.2,
        max_output_tokens: int = 2048,
    ) -> str:
        from backend.services.llm import GeminiClient

        client = GeminiClient()
        return client.generate(prompt, system=system)

    def embed_texts(self, texts: Iterable[str]) -> List[List[float]]:
        return [[float(len(t))] for t in texts]

    def health(self) -> Dict[str, Any]:
        return {"provider": self.provider, "ready": self.init_error is None}
