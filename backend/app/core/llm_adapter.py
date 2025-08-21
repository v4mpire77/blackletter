# Gemini-only LLM adapter
# Removes OpenAI/Ollama. Reads GEMINI_API_KEY and optional GEMINI_MODEL.

from __future__ import annotations
import os
from typing import Iterable, List, Optional, Dict, Any

import google.generativeai as genai


DEFAULT_GEN_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
DEFAULT_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "text-embedding-004")


class LLMAdapter:
    """
    Thin wrapper around Google Gemini for text generation and embeddings.

    Usage:
        llm = LLMAdapter()  # requires GEMINI_API_KEY in env
        text = llm.generate("Summarise this clause ...")
        vecs = llm.embed_texts(["hello", "world"])
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        gen_model: Optional[str] = None,
        embed_model: Optional[str] = None,
        temperature: float = 0.2,
        max_output_tokens: int = 2048,
    ) -> None:
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY is missing. Set it in your environment.")

        genai.configure(api_key=key)
        self.gen_model = gen_model or DEFAULT_GEN_MODEL
        self.embed_model = embed_model or DEFAULT_EMBED_MODEL
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    # --------- Health / readiness ---------
    def ready(self) -> bool:
        # Basic check: key configured and models are non-empty
        return bool(self.gen_model and self.embed_model)

    def health(self) -> Dict[str, Any]:
        return {
            "provider": "gemini",
            "ready": self.ready(),
            "gen_model": self.gen_model,
            "embed_model": self.embed_model,
        }

    # --------- Text generation ---------
    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: Optional=float,
        max_output_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate text from Gemini. If `system` is provided, it is used as a system instruction.
        """
        model = genai.GenerativeModel(
            model_name=self.gen_model,
            system_instruction=system if system else None,
        )
        resp = model.generate_content(
            prompt,
            generation_config={
                "temperature": self.temperature if temperature is None else float(temperature),
                "max_output_tokens": int(max_output_tokens or self.max_output_tokens),
            },
        )
        # Gemini SDK returns candidates; `.text` is a convenience property.
        return (resp.text or "").strip()

    # --------- Embeddings ---------
    def embed_text(self, text: str) -> List[float]:
        r = genai.embed_content(model=self.embed_model, content=text)
        return r["embedding"]["values"]

    def embed_texts(self, texts: Iterable[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]
