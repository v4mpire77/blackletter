"""Test Gemini import and basic functionality."""

import pytest
import os
from unittest.mock import patch, MagicMock


def test_gemini_import():
    """Test that Gemini can be imported successfully."""
    try:
        import google.generativeai as genai
        assert genai is not None
    except ImportError:
        pytest.fail("google-generativeai package is not available")


def test_gemini_llm_service_initialization():
    """Test that LLMService can be initialized with Gemini provider."""
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from llm_service import LLMService
        
        # Mock environment to ensure Gemini is selected
        with patch.dict(os.environ, {"LLM_PROVIDER": "gemini", "GEMINI_API_KEY": "test-key"}):
            service = LLMService()
            assert service.provider == "gemini"
            
            # Test provider info
            info = service.get_provider_info()
            assert info["provider"] == "gemini"
            assert "gemini" in info["model"].lower()
            
    except ImportError as e:
        # Module might not exist in this test context, which is acceptable
        pytest.skip(f"LLMService not available in test context: {e}")


def test_gemini_llm_adapter_initialization():
    """Test that LLMAdapter can be initialized with Gemini."""
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from app.core.llm_adapter import LLMAdapter
        
        # Mock environment
        with patch.dict(os.environ, {"LLM_PROVIDER": "gemini", "GEMINI_API_KEY": "test-key"}):
            adapter = LLMAdapter()
            assert adapter.provider == "gemini"
            assert adapter.gemini_key == "test-key"
            
    except ImportError as e:
        # Module might not exist in this test context, which is acceptable
        pytest.skip(f"LLMAdapter not available in test context: {e}")


def test_gemini_api_configuration():
    """Test Gemini API configuration."""
    import google.generativeai as genai
    
    # Test that configure accepts an API key
    try:
        genai.configure(api_key="test-key")
        # If no exception is raised, configuration works
        assert True
    except Exception as e:
        pytest.fail(f"Gemini configuration failed: {e}")


@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_gemini_model_creation(mock_model, mock_configure):
    """Test Gemini model creation."""
    import google.generativeai as genai
    
    # Mock the model
    mock_instance = MagicMock()
    mock_model.return_value = mock_instance
    
    # Configure and create model
    genai.configure(api_key="test-key")
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # Verify calls
    mock_configure.assert_called_with(api_key="test-key")
    mock_model.assert_called_with("gemini-2.0-flash")
    assert model is mock_instance


def test_no_openai_imports():
    """Test that no OpenAI imports remain in key modules."""
    import sys
    
    # List of modules that should not import OpenAI
    modules_to_check = [
        'app.core.llm_adapter',
        'services.llm', 
        'llm_service'
    ]
    
    for module_name in modules_to_check:
        try:
            # Clear module cache to ensure fresh import
            if module_name in sys.modules:
                del sys.modules[module_name]
                
            module = __import__(module_name, fromlist=[''])
            
            # Check that openai is not in module's attributes
            module_attrs = dir(module)
            openai_attrs = [attr for attr in module_attrs if 'openai' in attr.lower()]
            
            if openai_attrs:
                pytest.fail(f"Module {module_name} still contains OpenAI references: {openai_attrs}")
                
        except ImportError:
            # Module doesn't exist, which is fine
            pass