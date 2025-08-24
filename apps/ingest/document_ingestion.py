"""Utilities for extracting text from various document formats.

This module provides helper functions for the Document Ingestion
component. It supports machine-readable PDFs, Microsoft Word documents
(DOCX), and scanned PDFs via OCR. An optional helper for PII redaction is
also included.
"""

from __future__ import annotations

import re
from typing import List

import fitz  # PyMuPDF
import pytesseract
from docx import Document
from pdf2image import convert_from_path


def extract_text_from_pdf(path: str) -> str:
    """Extract text from a machine-readable PDF.

    Opens the PDF with PyMuPDF and concatenates text from all pages into a
    single string.
    """

    text = ""
    doc = fitz.open(path)
    for page in doc:
        page_text = page.get_text()
        if not page_text.strip():
            # Fallback to OCR for image-only pages
            images = convert_from_path(
                path, first_page=page.number + 1, last_page=page.number + 1
            )
            page_text = pytesseract.image_to_string(images[0])
        text += page_text
    return text


def extract_text_from_docx(path: str) -> str:
    """Extract text from a DOCX file."""

    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def ocr_pdf(path: str) -> str:
    """Run OCR on each page of a PDF and aggregate the text.

    Adds page markers to preserve structure in the resulting text.
    """

    images = convert_from_path(path)
    text_pages: List[str] = []
    for i, img in enumerate(images, start=1):
        txt = pytesseract.image_to_string(img)
        text_pages.append(f"[[Page {i}]]\n{txt}")
    return "\n".join(text_pages)


_PII_PATTERNS = [
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "[EMAIL]"),
    (re.compile(r"\+?\d[\d\s().-]{7,}\d"), "[PHONE]"),
]


def redact_pii(text: str) -> str:
    """Redact simple PII patterns from text."""

    for pattern, replacement in _PII_PATTERNS:
        text = pattern.sub(replacement, text)
    return text
