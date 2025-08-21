import os

ENABLE_OCR = os.getenv("ENABLE_OCR", "false").lower() in {"1", "true", "yes"}

def ocr_available() -> bool:
    """Check if OCR functionality is available."""
    return ENABLE_OCR

def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract text from image bytes using OCR.
    
    Args:
        image_bytes: Raw image data as bytes
        
    Returns:
        Extracted text from the image
        
    Raises:
        RuntimeError: If OCR is disabled or dependencies are missing
    """
    if not ENABLE_OCR:
        raise RuntimeError("OCR is disabled. Set ENABLE_OCR=true and install OCR deps.")
    
    try:
        from PIL import Image
        import io
        import pytesseract
    except ImportError as e:
        raise RuntimeError(f"OCR dependencies not installed. Run: pip install -r requirements-ocr.txt. Missing: {e}")
    
    img = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(img)

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file using pdfplumber with optional OCR fallback.
    
    Args:
        file_content: Raw PDF data as bytes
        
    Returns:
        Extracted text from the PDF
        
    Raises:
        RuntimeError: If OCR is disabled or dependencies are missing
    """
    if not ENABLE_OCR:
        raise RuntimeError("OCR is disabled. Set ENABLE_OCR=true and install OCR deps.")
    
    try:
        import pdfplumber
        import pytesseract
        from PIL import Image
        import io
    except ImportError as e:
        raise RuntimeError(f"OCR dependencies not installed. Run: pip install -r requirements-ocr.txt. Missing: {e}")
    
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        text_content = []

        for page in pdf.pages:
            text = page.extract_text() or ""
            if len(text.strip()) < 50:  # Arbitrary threshold for OCR fallback
                img = page.to_image()
                pil_image = Image.frombytes(
                    mode="RGB",
                    size=(img.width, img.height),
                    data=img.original.tobytes(),
                )
                text = pytesseract.image_to_string(pil_image) or ""

            text_content.append(text.strip())

        return "\n\n".join(text_content)