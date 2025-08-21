def analyze_contract_with_llm(text, filename):
    # Minimal stub for Gemini chat model integration
    # Replace this with actual Gemini API logic as needed
    return [
        {
            "issue": "Gemini chat model integration placeholder.",
            "details": f"Analyzed {filename} with Gemini. Text length: {len(text)}"
        }
    ]
import os
from typing import Any, Dict, List, Optional


class LLMAdapter:
    """Minimal adapter providing Gemini-only functionality for tests."""

    def __init__(self) -> None:
        # Default to Gemini so missing API keys surface clearly in tests
        self.provider = (os.getenv("LLM_PROVIDER") or "gemini").lower()
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.ollama_reachable = False
        self.init_error: Optional[str] = None

        if self.provider == "gemini":
            if not self.gemini_key:
                # CI expects a RuntimeError when no key is configured
                raise RuntimeError("GEMINI_API_KEY is missing")
        elif self.provider != "stub":
            # For unknown providers fall back to stub and record an error
            self.init_error = f"Unknown provider: {self.provider}"
            self.provider = "stub"

    # ------------------------------------------------------------------
    # Basic capability stubs used by tests and service wrappers
    # ------------------------------------------------------------------
    def health(self) -> Dict[str, Any]:
        ready = self.provider != "gemini" or bool(self.gemini_key)
        return {"provider": self.provider, "ready": ready, "model": self.model}

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.2,
        max_output_tokens: int = 2048,
    ) -> str:
        """Return a deterministic string for tests."""
        return prompt

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Return zero vectors for deterministic embedding tests."""
        return [[0.0] for _ in texts]

    async def analyze_contract(self, contract_text: str) -> Dict[str, Any]:
        """Very small async shim used by the service layer tests."""
        summary = (contract_text[:400] + "…") if len(contract_text) > 400 else contract_text
        return {"summary": summary, "risks": [], "dates": [], "error": self.init_error}

    def summarize(self, text: str) -> Dict[str, Any]:
        """Heuristic summariser used by legacy tests."""
        if self.provider == "stub":
            risks: List[Dict[str, str]] = []
            lowered = text.lower()
            if "data" in lowered or "personal" in lowered:
                risks.append({
                    "type": "GDPR",
                    "severity": "Medium",
                    "note": "Possible personal data processing without clarity on lawful basis.",
                })
            if "liability" in lowered:
                risks.append({
                    "type": "Liability",
                    "severity": "High",
                    "note": "Liability clause may be unbalanced.",
                })
            return {
                "summary": (text[:400] + "…") if len(text) > 400 else text,
                "risks": risks,
            }

        return {"summary": text[:400], "risks": []}
