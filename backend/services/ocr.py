import os
from typing import Optional

# Enable with: ENABLE_OCR=true
ENABLE_OCR = os.getenv("ENABLE_OCR", "false").lower() in {"1", "true", "yes"}

def ocr_available() -> bool:
    """Return True if OCR functionality is enabled by flag."""
    return ENABLE_OCR

def extract_text_from_image(image_bytes: bytes, lang: Optional[str] = None) -> str:
    """
    Extract text using Tesseract OCR. Requires:
      - Python deps in backend/requirements-ocr.txt
      - System binary: tesseract-ocr
    """
    if not ENABLE_OCR:
        raise RuntimeError("OCR is disabled. Set ENABLE_OCR=true and install OCR deps.")

    # Lazy imports so startup never fails if OCR deps aren't present
    from PIL import Image  # type: ignore
    import io
    import pytesseract  # type: ignore

    img = Image.open(io.BytesIO(image_bytes))
    config = f"-l {lang}" if lang else ""
    return pytesseract.image_to_string(img, config=config).strip()