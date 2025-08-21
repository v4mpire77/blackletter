"""
LLM Service module providing a unified interface for contract analysis.

This module wraps the existing LLMAdapter to provide a consistent interface
for testing and use throughout the application.
"""

import os
import asyncio
from app.core.llm_adapter import LLMAdapter


class LLMService:
    """
    Service class for LLM operations, particularly contract analysis.
    
    This class provides a simple interface to interact with various LLM providers
    (Gemini, OpenAI, Ollama) through the underlying LLMAdapter.
    """
    
    def __init__(self):
        """Initialize the LLM service with the configured adapter."""
        self.adapter = LLMAdapter()
        self.provider = self.adapter.provider
        
        # Check if there are any initialization errors
        if self.adapter.init_error:
            print(f"⚠️  Warning: {self.adapter.init_error}")
    
    async def analyze_contract(self, contract_text: str) -> dict:
        """
        Analyze a contract and return structured results.
        
        Args:
            contract_text (str): The contract text to analyze
            
        Returns:
            dict: Analysis results with keys like 'summary', 'risks', 'dates', etc.
        """
        return await self.adapter.analyze_contract(contract_text)
    
    def get_provider_info(self) -> dict:
        """
        Get information about the current LLM provider configuration.
        
        Returns:
            dict: Provider information including name, model, and status
        """
        return {
            "provider": self.adapter.provider,
            "model": self.adapter.model,
            "gemini_configured": bool(self.adapter.gemini_key),
            "ollama_available": self.adapter.ollama_reachable,
            "init_error": self.adapter.init_error
        }