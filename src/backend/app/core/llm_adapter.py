"""
LLM Adapter module for Blackletter Systems.

This module provides a unified interface for different LLM providers:
- OpenAI
- Anthropic
- Ollama (local)

Usage:
    from app.core.llm_adapter import get_llm_provider, generate
    
    # Get the configured LLM provider
    llm = get_llm_provider()
    
    # Generate text with the default model
    response = await generate(
        text="Summarize this contract",
        system="You are a legal assistant",
    )
    
    # Or specify a model
    response = await generate(
        text="Summarize this contract",
        system="You are a legal assistant",
        model="llama3.1:8b",
    )
"""

import os
from enum import Enum
from typing import Dict, Optional, Any, Union
import httpx
import json
import logging

# Import provider libraries
import openai
from anthropic import AsyncAnthropic
import ollama

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"

# Default models for each provider
DEFAULT_MODELS = {
    LLMProvider.OPENAI: "gpt-4o",
    LLMProvider.ANTHROPIC: "claude-3-opus-20240229",
    LLMProvider.OLLAMA: "llama3.1:8b",
}

# Environment configuration
PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_LLM = os.getenv("DEFAULT_LLM", DEFAULT_MODELS.get(PROVIDER, "llama3.1:8b"))

# Client instances
_openai_client = None
_anthropic_client = None
_ollama_client = None

def get_llm_provider() -> LLMProvider:
    """
    Get the configured LLM provider from environment.
    
    Returns:
        LLMProvider: The configured LLM provider
    """
    if PROVIDER == LLMProvider.OPENAI:
        return LLMProvider.OPENAI
    elif PROVIDER == LLMProvider.ANTHROPIC:
        return LLMProvider.ANTHROPIC
    elif PROVIDER == LLMProvider.OLLAMA:
        return LLMProvider.OLLAMA
    else:
        logger.warning(f"Unknown LLM provider: {PROVIDER}, defaulting to Ollama")
        return LLMProvider.OLLAMA

def _get_openai_client():
    """Get or initialize OpenAI client"""
    global _openai_client
    if _openai_client is None:
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not provided")
        _openai_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
    return _openai_client

def _get_anthropic_client():
    """Get or initialize Anthropic client"""
    global _anthropic_client
    if _anthropic_client is None:
        if not ANTHROPIC_API_KEY:
            raise ValueError("Anthropic API key not provided")
        _anthropic_client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    return _anthropic_client

def _get_ollama_client():
    """Get or initialize Ollama client"""
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = httpx.AsyncClient(base_url=OLLAMA_BASE_URL)
    return _ollama_client

async def _generate_openai(
    text: str, 
    system: str, 
    model: Optional[str] = None
) -> str:
    """Generate text using OpenAI"""
    client = _get_openai_client()
    model = model or DEFAULT_MODELS[LLMProvider.OPENAI]
    
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text}
        ],
        temperature=0.1,
    )
    
    return response.choices[0].message.content

async def _generate_anthropic(
    text: str, 
    system: str, 
    model: Optional[str] = None
) -> str:
    """Generate text using Anthropic"""
    client = _get_anthropic_client()
    model = model or DEFAULT_MODELS[LLMProvider.ANTHROPIC]
    
    response = await client.messages.create(
        model=model,
        system=system,
        messages=[
            {"role": "user", "content": text}
        ],
        temperature=0.1,
    )
    
    return response.content[0].text

async def _generate_ollama(
    text: str, 
    system: str, 
    model: Optional[str] = None
) -> str:
    """Generate text using Ollama"""
    client = _get_ollama_client()
    model = model or DEFAULT_MODELS[LLMProvider.OLLAMA]
    
    payload = {
        "model": model,
        "prompt": text,
        "system": system,
        "stream": False,
        "options": {
            "temperature": 0.1,
        }
    }
    
    response = await client.post("/api/generate", json=payload)
    response.raise_for_status()
    result = response.json()
    
    return result.get("response", "")

async def generate(
    text: str, 
    system: str, 
    model: Optional[str] = None,
    provider: Optional[LLMProvider] = None
) -> str:
    """
    Generate text using the configured LLM provider.
    
    Args:
        text: The prompt text to send to the LLM
        system: The system prompt to guide the LLM
        model: Optional model name to use (defaults to provider's default)
        provider: Optional provider override (defaults to configured provider)
        
    Returns:
        str: The generated text response
    
    Raises:
        ValueError: If the provider is not supported or API keys are missing
        httpx.HTTPError: If there's an issue with the API request
    """
    provider = provider or get_llm_provider()
    model = model or DEFAULT_LLM
    
    try:
        if provider == LLMProvider.OPENAI:
            return await _generate_openai(text, system, model)
        elif provider == LLMProvider.ANTHROPIC:
            return await _generate_anthropic(text, system, model)
        elif provider == LLMProvider.OLLAMA:
            return await _generate_ollama(text, system, model)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    except Exception as e:
        logger.error(f"Error generating text with {provider}: {str(e)}")
        raise