from __future__ import annotations
import os
import logging
from typing import List, Optional


# --- Gemini ---
import google.generativeai as genai

log = logging.getLogger("llm")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

class TransientLLMError(Exception):
    pass
class GeminiClient:
    def __init__(self, model: Optional[str] = None):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY missing")
        genai.configure(api_key=api_key)
        model_name = model or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Generate text from a prompt with optional system instruction."""
        pre = f"System: {system}\n\n" if system else ""
        resp = self.model.generate_content(pre + prompt)
        return getattr(resp, "text", "").strip()

    def chat(self, messages: List[dict]) -> str:
        """Chat with a list of messages in OpenAI format."""
        # Convert OpenAI-style messages to Gemini format
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        full_prompt = "\n\n".join(prompt_parts)
        resp = self.model.generate_content(full_prompt)
        return getattr(resp, "text", "").strip()

# Backward-compatible alias
LLMClient = GeminiClient

# Compatibility function for existing code
def generate_text(prompt: str, *, system: Optional[str] = None, max_tokens: int = 800) -> str:
    """Generate text using Gemini client. Compatibility wrapper for existing code."""
    client = GeminiClient()
    return client.generate(prompt, system=system)
