"""Test Gemini client import and runtime functionality."""
import pytest
from unittest.mock import Mock, patch
from ..services.llm import GeminiClient, LLMClient


def test_gemini_client_import():
    """Test that GeminiClient can be imported."""
    assert GeminiClient is not None
    assert callable(GeminiClient)


def test_llm_client_alias():
    """Test that LLMClient is an alias for GeminiClient."""
    assert LLMClient is GeminiClient


@patch('services.llm.genai')
@patch('services.llm.os.getenv')
def test_gemini_client_instantiation(mock_getenv, mock_genai):
    """Test proper instantiation of GeminiClient."""
    # Mock environment variables
    mock_getenv.side_effect = lambda key, default=None: {
        'GEMINI_API_KEY': 'test-api-key',
        'GEMINI_MODEL': 'gemini-1.5-flash'
    }.get(key, default)
    
    # Mock Gemini SDK
    mock_model = Mock()
    mock_genai.GenerativeModel.return_value = mock_model
    
    client = GeminiClient()
    
    # Verify API key configuration
    mock_genai.configure.assert_called_once_with(api_key='test-api-key')
    # Verify model instantiation
    mock_genai.GenerativeModel.assert_called_once_with('gemini-1.5-flash')
    assert client.model is mock_model


@patch('services.llm.genai')
@patch('services.llm.os.getenv')
def test_gemini_client_generate_method(mock_getenv, mock_genai):
    """Test GeminiClient generate method."""
    # Mock environment variables
    mock_getenv.side_effect = lambda key, default=None: {
        'GEMINI_API_KEY': 'test-api-key',
        'GEMINI_MODEL': 'gemini-1.5-flash'
    }.get(key, default)
    
    # Mock Gemini SDK
    mock_response = Mock()
    mock_response.text = "Generated response text"
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model
    
    client = GeminiClient()
    result = client.generate("Test prompt", system="Test system instruction")
    
    # Verify method was called with correct prompt format
    expected_prompt = "System: Test system instruction\n\nTest prompt"
    mock_model.generate_content.assert_called_once_with(expected_prompt)
    assert result == "Generated response text"


@patch('services.llm.genai')
@patch('services.llm.os.getenv')
def test_gemini_client_chat_method(mock_getenv, mock_genai):
    """Test GeminiClient chat method."""
    # Mock environment variables
    mock_getenv.side_effect = lambda key, default=None: {
        'GEMINI_API_KEY': 'test-api-key',
        'GEMINI_MODEL': 'gemini-1.5-flash'
    }.get(key, default)
    
    # Mock Gemini SDK
    mock_response = Mock()
    mock_response.text = "Chat response text"
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model
    
    client = GeminiClient()
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "How are you?"}
    ]
    result = client.chat(messages)
    
    # Verify method was called with correct prompt format
    expected_prompt = (
        "System: You are a helpful assistant\n\n"
        "User: Hello\n\n"
        "Assistant: Hi there!\n\n"
        "User: How are you?"
    )
    mock_model.generate_content.assert_called_once_with(expected_prompt)
    assert result == "Chat response text"


@patch('services.llm.os.getenv')
def test_gemini_client_missing_api_key(mock_getenv):
    """Test that GeminiClient raises error when API key is missing."""
    mock_getenv.return_value = None  # No API key
    
    with pytest.raises(RuntimeError, match="GEMINI_API_KEY missing"):
        GeminiClient()


@patch('services.llm.genai')
@patch('services.llm.os.getenv')
def test_gemini_client_custom_model(mock_getenv, mock_genai):
    """Test GeminiClient with custom model parameter."""
    # Mock environment variables
    mock_getenv.side_effect = lambda key, default=None: {
        'GEMINI_API_KEY': 'test-api-key',
        'GEMINI_MODEL': 'gemini-1.5-flash'  # This should be overridden
    }.get(key, default)
    
    # Mock Gemini SDK
    mock_model = Mock()
    mock_genai.GenerativeModel.return_value = mock_model
    
    client = GeminiClient(model="gemini-pro")
    
    # Verify custom model was used
    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')