"""
Enhanced OCR processor module for real PDF text extraction using pytesseract and pdfplumber.
"""
import os
import io
import platform
import asyncio
from typing import Optional

try:
    import pdfplumber
    import pytesseract
    from PIL import Image
    HAS_OCR_DEPS = True
except ImportError:
    HAS_OCR_DEPS = False


class OCRProcessor:
    def __init__(self):
        """Configure pytesseract based on the current platform."""
        if not HAS_OCR_DEPS:
            raise ImportError(
                "OCR dependencies not installed. Run: pip install pdfplumber pytesseract pillow"
            )
            
        tesseract_cmd = os.getenv("TESSERACT_CMD")

        if not tesseract_cmd:
            system = platform.system()
            if system == "Windows":
                tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            elif system == "Darwin":  # macOS
                tesseract_cmd = "/usr/local/bin/tesseract"
            else:  # Assume Linux/Unix
                tesseract_cmd = "/usr/bin/tesseract"

        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def _process_pdf(self, file_content: bytes) -> str:
        """Blocking PDF/OCR logic split into a helper for thread execution."""
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            text_content = []

            for page in pdf.pages:
                # Extract text content
                text = page.extract_text() or ""
                
                # If page has little or no text, try OCR on the page image
                if len(text.strip()) < 50:  # Arbitrary threshold
                    img = page.to_image()
                    # pdfplumber's PageImage exposes the underlying PIL image via
                    # the "original" attribute. The previous approach attempted to
                    # rebuild the image from raw bytes and referenced attributes that
                    # do not exist on PageImage, causing an AttributeError. Using the
                    # original image directly avoids this issue.
                    pil_image = img.original if hasattr(img, "original") else img
                    # Perform OCR
                    text = pytesseract.image_to_string(pil_image) or ""

                text_content.append(text.strip())

            return "\n\n".join(text_content)

    async def extract_text(self, file_content: bytes) -> str:
        """Extract text from a PDF file using pdfplumber and pytesseract for images."""
        try:
            return await asyncio.to_thread(self._process_pdf, file_content)
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")


def perform_ocr(file_bytes: bytes, filename: Optional[str] = None) -> str:
    """
    Extract text from a PDF file using enhanced OCR processing.
    
    Args:
        file_bytes: Raw bytes of the PDF file
        filename: Optional filename for context
        
    Returns:
        Extracted text from the document
    """
    if not HAS_OCR_DEPS:
        # Fallback to simulation if dependencies not available
        from .ocr import perform_ocr as simulate_ocr
        return simulate_ocr(file_bytes, filename)
    
    try:
        processor = OCRProcessor()
        # Since we need to run this synchronously in the current context,
        # we'll create a new event loop if needed
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(processor.extract_text(file_bytes))
    except Exception as e:
        # Fallback to simulation on error
        from .ocr import perform_ocr as simulate_ocr
        print(f"OCR processing failed, falling back to simulation: {e}")
        return simulate_ocr(file_bytes, filename)
