import os
import json
import asyncio
from typing import Optional, Any, List
import numpy as np

try:
    import openai
except Exception:
    openai = None

try:
    import ollama
except Exception:
    ollama = None

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

import requests


class LLMAdapter:
    """Async adapter supporting OpenAI and Ollama (HTTP fallback).

    It prefers OpenAI when LLM_PROVIDER=openai and OPENAI_API_KEY is set. For Ollama it will
    try the python package then fall back to the HTTP API at OLLAMA_BASE_URL.
    """

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama")
        self.model = os.getenv(
            "DEFAULT_LLM", "llama3.1:8b" if self.provider == "ollama" else "gpt-4"
        )
        self.ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.openai_key = os.getenv("OPENAI_API_KEY")

        # Check whether an Ollama server is reachable
        self.ollama_reachable = self._ollama_ready()

        if self.provider == "openai" and openai is not None and self.openai_key:
            openai.api_key = self.openai_key

        # Initialize embedding model
        self.embedding_model = None
        self._init_embedding_model()

        # Record a clear error if neither backend is available
        self.init_error: Optional[str] = None
        if not self.openai_key and not self.ollama_reachable:
            self.init_error = (
                f"No LLM backend configured. Set OPENAI_API_KEY or start an Ollama server at {self.ollama_base}."
            )

    def _init_embedding_model(self):
        """Initialize the embedding model for RAG functionality."""
        try:
            if SentenceTransformer is not None:
                # Use a good general-purpose embedding model
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            else:
                print("Warning: sentence-transformers not available. Embeddings will use fallback method.")
        except Exception as e:
            print(f"Warning: Could not initialize embedding model: {e}")

    def _ollama_ready(self) -> bool:
        """Check if an Ollama server responds to a simple request."""
        try:
            url = self.ollama_base.rstrip("/") + "/api/tags"
            requests.get(url, timeout=2)
            return True
        except Exception:
            return False

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        # Use sentence-transformers if available
        if self.embedding_model is not None:
            def sync_embed():
                embeddings = self.embedding_model.encode(texts, convert_to_tensor=False)
                return embeddings.tolist() if hasattr(embeddings, 'tolist') else embeddings
            
            return await asyncio.to_thread(sync_embed)
        
        # Fallback: use OpenAI embeddings if available
        elif self.openai_key and openai is not None:
            try:
                def sync_openai_embed():
                    response = openai.Embedding.create(
                        input=texts,
                        model="text-embedding-ada-002"
                    )
                    return [data.embedding for data in response.data]
                
                return await asyncio.to_thread(sync_openai_embed)
            except Exception as e:
                print(f"OpenAI embedding failed: {e}")
        
        # Final fallback: simple hash-based embeddings (not recommended for production)
        print("Warning: Using fallback embedding method. Install sentence-transformers for better results.")
        return [self._fallback_embedding(text) for text in texts]
    
    def _fallback_embedding(self, text: str) -> List[float]:
        """Simple fallback embedding method using hash."""
        import hashlib
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()
        # Convert to 384-dimensional vector (matching all-MiniLM-L6-v2)
        embedding = []
        for i in range(384):
            embedding.append(float(hash_bytes[i % 16]) / 255.0)
        return embedding

    async def _call_openai(self, messages: list) -> str:
        if openai is None:
            raise RuntimeError("openai package not available")
        # run in thread to avoid blocking event loop
        def sync_call():
            # Support both new OpenAI and older ChatCompletion shapes
            resp = None
            create = getattr(openai, "ChatCompletion", None)
            if create is not None:
                resp = create.create(model=self.model, messages=messages)
                # Try different access patterns
                if hasattr(resp, "choices"):
                    choice = resp.choices[0]
                    if hasattr(choice, "message"):
                        return getattr(choice.message, "content", "")
                    return getattr(choice, "text", "")

            # Fallback to chat completions via client method
            try:
                client_chat = getattr(openai, "chat", None)
                if client_chat is not None and hasattr(client_chat, "completions"):
                    resp = client_chat.completions.create(model=self.model, messages=messages)
                    if resp and hasattr(resp, "choices"):
                        return getattr(resp.choices[0].message, "content", "")
            except Exception:
                pass

            # Last resort: stringify whatever we have
            return str(resp or "")

        return await asyncio.to_thread(sync_call)

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
        resp = requests.post(url, json={"model": self.model, "messages": messages}, timeout=30)
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

    async def generate_with_context(self, query: str, context_chunks: List[str], 
                                  max_tokens: int = 1000) -> str:
        """
        Generate a response using RAG context.
        
        Args:
            query: User query
            context_chunks: Retrieved context chunks
            max_tokens: Maximum tokens for response
            
        Returns:
            Generated response
        """
        context_text = "\n\n".join(context_chunks)
        
        system_prompt = """You are a legal contract analysis assistant. Use the provided context to answer questions accurately and comprehensively. If the context doesn't contain enough information to answer the question, say so clearly.

Guidelines:
- Base your answers on the provided context
- Be precise and cite specific parts of the contract when relevant
- If asked about risks or compliance issues, be thorough
- Maintain a professional tone
- If you're unsure about something, acknowledge the uncertainty"""

        user_prompt = f"""Context from contract:
{context_text}

Question: {query}

Please provide a detailed answer based on the context above."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        if self.init_error:
            return f"Error: {self.init_error}"

        # Prefer provider, but fall back gracefully if unavailable
        if self.provider == "openai":
            if self.openai_key and openai is not None:
                resp = await self._call_openai(messages)
            elif self.ollama_reachable:
                resp = await self._call_ollama(messages)
            else:
                return f"Error: OPENAI_API_KEY is missing and no Ollama server reachable at {self.ollama_base}."
        else:
            if self.ollama_reachable:
                resp = await self._call_ollama(messages)
            elif self.openai_key and openai is not None:
                resp = await self._call_openai(messages)
            else:
                return f"Error: {self.init_error}"

        return resp

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
            return {"summary": "", "risks": [], "dates": [], "error": self.init_error}

        # Prefer provider, but fall back gracefully if unavailable
        if self.provider == "openai":
            if self.openai_key and openai is not None:
                resp = await self._call_openai(messages)
            elif self.ollama_reachable:
                resp = await self._call_ollama(messages)
            else:
                return {
                    "summary": "",
                    "risks": [],
                    "dates": [],
                    "error": f"OPENAI_API_KEY is missing and no Ollama server reachable at {self.ollama_base}.",
                }
        else:
            if self.ollama_reachable:
                resp = await self._call_ollama(messages)
            elif self.openai_key and openai is not None:
                resp = await self._call_openai(messages)
            else:
                return {
                    "summary": "",
                    "risks": [],
                    "dates": [],
                    "error": self.init_error,
                }

        # Attempt to parse JSON
        try:
            return json.loads(resp)
        except Exception:
            return resp

