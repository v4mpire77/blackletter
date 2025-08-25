from typing import List

from ..document_ingestion import extract_text_from_docx, redact_pii
from ..models import ContractChunk
from ..utils import count_tokens, new_id, split_into_sections


def ingest(path: str, contract_id: str) -> List[ContractChunk]:
    text = redact_pii(extract_text_from_docx(path))
    chunks: List[ContractChunk] = []
    for section, section_text in split_into_sections(text):
        chunk = ContractChunk(
            id=new_id(),
            contract_id=contract_id,
            section=section,
            text=section_text,
            page=1,
            tokens=count_tokens(section_text),
        )
        chunks.append(chunk)
    return chunks
