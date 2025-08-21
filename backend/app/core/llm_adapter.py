import os
import json
import asyncio
import re
from typing import Optional, Any

try:
    import ollama
except Exception:
    ollama = None

import httpx


class LLMAdapter:
    """Async adapter supporting Gemini and Ollama (HTTP fallback).

    Set ``LLM_PROVIDER=gemini`` with ``GEMINI_API_KEY`` for Gemini. For Ollama it will try
    the python package then fall back to the HTTP API at ``OLLAMA_BASE_URL``.
    """

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "gemini")
        if self.provider == "gemini":
            default_model = "gemini-1.5-flash"
        else:
            default_model = "llama3.1:8b"
        self.model = os.getenv("DEFAULT_LLM", default_model)

        self.ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.gemini_key = os.getenv("GEMINI_API_KEY")

        # Check whether an Ollama server is reachable
        self.ollama_reachable = self._ollama_ready()

        # Record a clear error if neither backend is available
        self.init_error: Optional[str] = None
        if self.provider == "gemini" and not self.gemini_key:
            self.init_error = "GEMINI_API_KEY is missing."
        elif self.provider == "ollama" and not self.ollama_reachable:
            self.init_error = f"Ollama server not reachable at {self.ollama_base}."
        elif not any([self.gemini_key, self.ollama_reachable]):
            self.init_error = (
                f"No LLM backend configured. Set GEMINI_API_KEY or start an Ollama server at {self.ollama_base}."
            )

    def _ollama_ready(self) -> bool:
        """Check if an Ollama server responds to a simple request."""
        try:
            url = self.ollama_base.rstrip("/") + "/api/tags"
            httpx.get(url, timeout=2)
            return True
        except Exception:
            return False

    async def chat(self, messages: list) -> str:
        """Chat with unified client interface."""
        from services.llm import GeminiClient
        
        if self.init_error:
            # Basic heuristic fallback
            return f"LLM unavailable: {self.init_error}"
        
        if self.provider == "gemini":
            client = GeminiClient()
            return client.chat(messages)
        elif self.provider == "ollama":
            return await self._call_ollama(messages)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Generate text with unified client interface."""
        from services.llm import GeminiClient
        
        if self.init_error:
            return f"LLM unavailable: {self.init_error}"
        
        if self.provider == "gemini":
            client = GeminiClient()
            return client.generate(prompt, system=system)
        elif self.provider == "ollama":
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            return await self._call_ollama(messages)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    async def _call_gemini(self, messages: list) -> str:
        if not self.gemini_key:
            raise RuntimeError("GEMINI_API_KEY is missing")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        contents = []
        for msg in messages:
            contents.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})
        payload = {"contents": contents}
        headers = {"X-goog-api-key": self.gemini_key}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

    async def _call_ollama(self, messages: list) -> str:
        # Prefer python client if available
        if ollama is not None:
            def sync_call():
                # use getattr to avoid static lint errors
                chat_fn = getattr(ollama, "chat", None)
                if chat_fn is not None:
                    res = chat_fn(model=self.model, messages=messages)
                    # handle different shapes
                    if isinstance(res, dict) and "message" in res:
                        return res["message"].get("content", "")
                    # try common attributes
                    if hasattr(res, "text"):
                        return getattr(res, "text")
                    return str(res)

                # try alternate client shape (guarded)
                chat_client_cls = getattr(ollama, "ChatClient", None)
                if callable(chat_client_cls):
                    try:
                        client = chat_client_cls()
                        if hasattr(client, "chat"):
                            res = getattr(client, "chat")(model=self.model, messages=messages)
                            return str(res)
                    except Exception:
                        pass

                return ""

            return await asyncio.to_thread(sync_call)

        # Fallback to HTTP
        url = self.ollama_base.rstrip("/") + "/api/chat"
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url, json={"model": self.model, "messages": messages}, timeout=30
            )
        resp.raise_for_status()
        body = resp.json()
        if isinstance(body, dict):
            if "response" in body:
                return body["response"]
            if "choices" in body and body["choices"]:
                choice = body["choices"][0]
                if isinstance(choice, dict):
                    return choice.get("message", {}).get("content", "") or choice.get("content", "")
        return json.dumps(body)

    async def analyze_contract(self, text: str) -> Any:
        """Analyze contract text and return either parsed JSON or raw text."""
        prompt = (
            "Analyze this contract text and provide:\n"
            "1. A brief summary (2-3 sentences)\n"
            "2. Key risks or concerns\n"
            "3. Important dates or deadlines\n\n"
            "Format as JSON with keys: summary (string), risks (list), dates (list).\n"
        )

        system = "You are a legal contract analysis assistant. Be concise and focus on material risks."
        user = f"{prompt}\nText: {text}"
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]

        if self.init_error:
            # Basic heuristic fallback so the system still returns something
            sentences = re.split(r"(?<=[.!?])\s+", text.strip())
            summary = " ".join(sentences[:2]).strip()
            risk_sentences = [
                s.strip()
                for s in sentences[2:]
                if re.search(r"\b(shall|must|obligation|liability|indemnify|terminate)\b", s, re.I)
            ]
            return {
                "summary": summary,
                "risks": risk_sentences[:5],
                "dates": [],
                "error": self.init_error,
            }

        # Route to configured provider
        try:
            resp = await self.chat(messages)
        except Exception as e:
            return {
                "summary": "",
                "risks": [],
                "dates": [],
                "error": str(e),
            }

        # Attempt to parse JSON
        try:
            return json.loads(resp)
        except Exception:
            return resp

