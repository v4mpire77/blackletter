import os
from typing import Dict, Any, List

class LLMAdapter:
    def __init__(self) -> None:
        self.provider = (os.getenv("LLM_PROVIDER") or "stub").lower()

    def summarize(self, text: str) -> Dict[str, Any]:
        """
        Return a deterministic structure the tests can assert on:
        {
          "summary": str,
          "risks": [{"type": "...","severity":"High|Medium|Low","note":"..."}]
        }
        """
        if self.provider == "stub":
            risks: List[Dict[str, str]] = []
            lowered = text.lower()
            # very simple heuristics to always return something predictable
            if "data" in lowered or "personal" in lowered:
                risks.append({"type": "GDPR", "severity": "Medium", "note": "Possible personal data processing without clarity on lawful basis."})
            if "liability" in lowered:
                risks.append({"type": "Liability", "severity": "High", "note": "Liability clause may be unbalanced."})
            return {
                "summary": (text[:400] + "…") if len(text) > 400 else text,
                "risks": risks,
            }

        # Future: add gemini/openai branches guarded by API keys
        return {"summary": text[:400], "risks": []}
