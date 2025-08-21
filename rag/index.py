"""Build local Chroma collections for contracts and authority documents."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable, List

import chromadb
import google.generativeai as genai
from pypdf import PdfReader
from docx import Document

# Default chunking parameters
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


def read_text(path: Path) -> str:
    """Extract plain text from supported file types."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if ext == ".docx":
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    if ext in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    if ext in {".html", ".htm"}:
        text = path.read_text(encoding="utf-8")
        # Strip simple HTML tags
        return re.sub("<[^>]+>", " ", text)
    return ""


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into simple character chunks with overlap."""
    chunks: List[str] = []
    step = chunk_size - overlap
    for i in range(0, len(text), step):
        chunk = text[i : i + chunk_size]
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)
    return chunks


def embed_texts(model: str, texts: List[str]) -> List[List[float]]:
    """Placeholder for text embeddings - Gemini doesn't provide embeddings API yet."""
    raise NotImplementedError(
        "Embedding functionality is not available with Gemini. "
        "This feature is disabled in the current Gemini-only configuration."
    )


def index_contracts(client: chromadb.PersistentClient, model: str, file_path: Path) -> int:
    """Index contract chunks from a JSONL file."""
    raise NotImplementedError(
        "Contract indexing is not available with Gemini. "
        "This feature is disabled in the current Gemini-only configuration."
    )


def index_authority(client: chromadb.PersistentClient, model: str, kb_dir: Path) -> int:
    """Index authority documents located in kb_dir."""
    raise NotImplementedError(
        "Authority document indexing is not available with Gemini. "
        "This feature is disabled in the current Gemini-only configuration."
    )


def main() -> None:
    print("RAG indexing is disabled in the current Gemini-only configuration.")
    print("Embedding functionality is not available with Gemini API.")
    return


if __name__ == "__main__":  # pragma: no cover
    main()
