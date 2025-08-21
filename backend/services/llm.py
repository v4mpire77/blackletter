from __future__ import annotations
import os
import logging
from dataclasses import dataclass
from typing import List, Optional

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# --- Gemini ---
import google.generativeai as genai
# --- OpenAI ---
from openai import OpenAI
from openai.types.chat import ChatCompletion
# --- Ollama ---
import requests

log = logging.getLogger("llm")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

@dataclass
class ModelPrefs:
    gemini: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    openai: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    ollama: str = os.getenv("OLLAMA_MODEL", "llama3.1")

def _provider_order() -> List[str]:
    order = os.getenv("PROVIDER_ORDER", "gemini,openai,ollama")
    return [p.strip().lower() for p in order.split(",") if p.strip()]

class GeminiClient:
    def __init__(self, model_name: str):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY missing")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt: str, system: Optional[str] = None, max_tokens: int = 800) -> str:
        pre = f"System: {system}\n\n" if system else ""
        resp = self.model.generate_content(pre + prompt)
        return getattr(resp, "text", "").strip()

class OpenAIClient:
    def __init__(self, model_name: str):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY missing")
        self.client = OpenAI(api_key=api_key)
        self.model = model_name

    def generate(self, prompt: str, system: Optional[str] = None, max_tokens: int = 800) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        r: ChatCompletion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            max_tokens=max_tokens,
        )
        return (r.choices[0].message.content or "").strip()

class OllamaClient:
    def __init__(self, model_name: str):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = model_name

    def generate(self, prompt: str, system: Optional[str] = None, max_tokens: int = 800) -> str:
        # Build prompt with system message if provided
        full_prompt = prompt
        if system:
            full_prompt = f"System: {system}\n\n{prompt}"
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result.get('response', '').strip()
        except Exception as e:
            raise RuntimeError(f"Ollama error: {str(e)}")

class TransientLLMError(Exception):
    pass

def _client_for(provider: str, models: ModelPrefs):
    if provider == "gemini":
        return GeminiClient(models.gemini)
    if provider == "openai":
        return OpenAIClient(models.openai)
    if provider == "ollama":
        return OllamaClient(models.ollama)
    raise ValueError(f"Unknown provider: {provider}")

@retry(
    retry=retry_if_exception_type(TransientLLMError),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=8),
    stop=stop_after_attempt(3),
)
def _try_generate(client, prompt: str, system: Optional[str], max_tokens: int) -> str:
    try:
        out = client.generate(prompt, system=system, max_tokens=max_tokens)
        if not out:
            raise TransientLLMError("Empty LLM response")
        return out
    except Exception as e:
        msg = str(e).lower()
        if any(k in msg for k in ["rate", "overload", "temporar", "timeout", "503", "429"]):
            raise TransientLLMError(msg)
        raise

def generate_text(prompt: str, *, system: Optional[str] = None, max_tokens: int = 800) -> str:
    models = ModelPrefs()
    last_err: Optional[Exception] = None
    for provider in _provider_order():
        try:
            client = _client_for(provider, models)
            log.info(f"LLM try provider={provider} model={getattr(models, provider)}")
            return _try_generate(client, prompt, system, max_tokens)
        except TransientLLMError as e:
            log.warning(f"Transient error on {provider}: {e}")
            last_err = e
            continue
        except Exception as e:
            log.error(f"Hard error on {provider}: {e}")
            last_err = e
            continue
    raise RuntimeError(f"All LLM providers failed: {last_err}")
