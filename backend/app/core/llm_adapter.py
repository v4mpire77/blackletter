import os
from typing import Optional
import ollama

class LLMAdapter:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama")
        self.model = os.getenv("DEFAULT_LLM", "llama3.1:8b")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        if self.provider == "ollama":
            ollama.base_url = self.ollama_base_url

    async def generate(self, text: str, system: Optional[str] = None) -> str:
        """Generate text using the configured LLM provider."""
        if self.provider == "ollama":
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system or "You are a helpful assistant."},
                    {"role": "user", "content": text}
                ]
            )
            return response['message']['content']
        
        raise ValueError(f"Unsupported LLM provider: {self.provider}")

    async def analyze_contract(self, text: str) -> dict:
        """Analyze contract text and return a risk-aware summary."""
        prompt = """Analyze this contract text and provide:
1. A brief summary (2-3 sentences)
2. Key risks or concerns
3. Important dates or deadlines

Format as JSON with keys: summary, risks (list), dates (list)
"""
        system = """You are a legal contract analysis assistant. Be concise and focus on material risks."""
        
        response = await self.generate(f"{prompt}\n\nText: {text}", system=system)
        # Note: In production, add proper JSON parsing and error handling
        return response
