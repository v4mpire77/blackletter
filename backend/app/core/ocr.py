from typing import Optional
import pdfplumber
import pytesseract
from PIL import Image
import io
import os
import platform

class OCRProcessor:
    def __init__(self):
        """Configure pytesseract based on the current platform."""
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

    async def extract_text(self, file_content: bytes) -> str:
        """Extract text from a PDF file using pdfplumber and pytesseract for images."""
        try:
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
                
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")
