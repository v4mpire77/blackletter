import asyncio
import os
import platform

# Feature flag for OCR availability
ENABLE_OCR = os.getenv("ENABLE_OCR", "false").lower() in {"1", "true", "yes"}

def ocr_available() -> bool:
    """Check if OCR functionality is available."""
    return ENABLE_OCR

class OCRProcessor:
    def __init__(self):
        """Configure pytesseract based on the current platform."""
        if not ENABLE_OCR:
            raise RuntimeError("OCR is disabled. Set ENABLE_OCR=true and install OCR deps.")
        
        try:
            import pytesseract
        except ImportError:
            raise RuntimeError("OCR dependencies not installed. Run: pip install -r requirements-ocr.txt")
        
        tesseract_cmd = os.getenv("TESSERACT_CMD")

        if not tesseract_cmd:
            system = platform.system()
            if system == "Windows":
                tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
            elif system == "Darwin":  # macOS
                tesseract_cmd = "/usr/local/bin/tesseract"
            else:  # Assume Linux/Unix
                tesseract_cmd = "/usr/bin/tesseract"

        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def _process_pdf(self, file_content: bytes) -> str:
        """Blocking PDF/OCR logic split into a helper for thread execution."""
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
                if len(text.strip()) < 50:  # Arbitrary threshold
                    img = page.to_image()
                    pil_image = Image.frombytes(
                        mode="RGB",
                        size=(img.width, img.height),
                        data=img.original.tobytes(),
                    )
                    text = pytesseract.image_to_string(pil_image) or ""

                text_content.append(text.strip())

            return "\n\n".join(text_content)

    async def extract_text(self, file_content: bytes) -> str:
        """Extract text from a PDF file using pdfplumber and pytesseract for images."""
        if not ENABLE_OCR:
            raise RuntimeError("OCR is disabled. Set ENABLE_OCR=true and install OCR deps.")
        
        try:
            return await asyncio.to_thread(self._process_pdf, file_content)
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")
