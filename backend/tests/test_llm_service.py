"""
Test module for the LLMService wrapper class.
"""

import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock, patch

# Add the parent directory to the path so we can import llm_service
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_service import LLMService


def test_llm_service_initialization():
    """Test that LLMService initializes correctly."""
    service = LLMService()
    assert hasattr(service, 'adapter')
    assert hasattr(service, 'provider')
    assert hasattr(service, 'analyze_contract')
    assert hasattr(service, 'get_provider_info')


def test_get_provider_info():
    """Test provider information retrieval."""
    service = LLMService()
    info = service.get_provider_info()
    
    required_keys = ["provider", "model", "gemini_configured", 
                    "ollama_available", "init_error"]
    
    for key in required_keys:
        assert key in info
    
    assert isinstance(info["gemini_configured"], bool)
    assert isinstance(info["ollama_available"], bool)


@pytest.mark.asyncio
async def test_analyze_contract():
    """Test contract analysis functionality."""
    service = LLMService()
    
    # Mock the adapter's analyze_contract method
    mock_result = {
        "summary": "Test summary",
        "risks": ["Test risk"],
        "dates": [],
        "error": None
    }
    
    with patch.object(service.adapter, 'analyze_contract', new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = mock_result
        
        result = await service.analyze_contract("Test contract text")
        
        assert result == mock_result
        mock_analyze.assert_called_once_with("Test contract text")


if __name__ == "__main__":
    # Run a simple test
    service = LLMService()
    print(f"✅ LLMService created successfully")
    print(f"Provider: {service.provider}")
    
    info = service.get_provider_info()
    print(f"Provider info keys: {list(info.keys())}")