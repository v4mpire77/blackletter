from typing import List

import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path

from ..document_ingestion import redact_pii
from ..models import ContractChunk
from ..utils import count_tokens, new_id, split_into_sections


def ingest(path: str, contract_id: str) -> List[ContractChunk]:
    doc = fitz.open(path)
    chunks: List[ContractChunk] = []
    for page_index in range(doc.page_count):
        page = doc[page_index]
        text = page.get_text() or ""
        if not text.strip():
            images = convert_from_path(
                path, first_page=page_index + 1, last_page=page_index + 1
            )
            text = pytesseract.image_to_string(images[0])
        text = redact_pii(text)
        for section, section_text in split_into_sections(text):
            chunk = ContractChunk(
                id=new_id(),
                contract_id=contract_id,
                section=section,
                text=section_text,
                page=page_index + 1,
                tokens=count_tokens(section_text),
            )
            chunks.append(chunk)
    return chunks
