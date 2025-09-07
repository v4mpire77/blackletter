from pathlib import Path

import fitz
from docx import Document

from apps.ingest.document_ingestion import (extract_text_from_docx,
                                            extract_text_from_pdf, redact_pii)


def test_extract_text_from_pdf(tmp_path: Path):
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello PDF")
    doc.save(pdf_path)

    text = extract_text_from_pdf(str(pdf_path))
    assert "Hello PDF" in text


def test_extract_text_from_docx(tmp_path: Path):
    docx_path = tmp_path / "sample.docx"
    doc = Document()
    doc.add_paragraph("Hello DOCX")
    doc.save(docx_path)

    text = extract_text_from_docx(str(docx_path))
    assert "Hello DOCX" in text


def test_redact_pii():
    text = "Reach me at john.doe@example.com or +1 555-123-4567."
    redacted = redact_pii(text)
    assert "[EMAIL]" in redacted
    assert "[PHONE]" in redacted
