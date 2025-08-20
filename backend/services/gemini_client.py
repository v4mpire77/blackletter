import os
import google.generativeai as genai

# Configure the client with the API key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Google's Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return the response text."""
    response = model.generate_content(prompt)
    return response.text
