import io
import os
import sys
from PIL import Image
import asyncio
import pytesseract

# Ensure the backend package is importable when tests are run from the repo root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.ocr import OCRProcessor


def test_extract_text_scanned_pdf(monkeypatch):
    # Create a simple PDF containing just an image so that OCR path is triggered
    img = Image.new("RGB", (100, 100), color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PDF")
    content = buffer.getvalue()

    # Avoid calling the real tesseract binary by monkeypatching
    monkeypatch.setattr(pytesseract, "image_to_string", lambda image: "dummy text")

    ocr = OCRProcessor()
    text = asyncio.run(ocr.extract_text(content))
    assert "dummy text" in text
