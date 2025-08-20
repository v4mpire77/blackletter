"""Build local Chroma collections for contracts and authority documents."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable, List

import chromadb
from openai import OpenAI
import tiktoken
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
    """Split text into token chunks with overlap."""
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    chunks: List[str] = []
    step = chunk_size - overlap
    for i in range(0, len(tokens), step):
        chunk_tokens = tokens[i : i + chunk_size]
        chunks.append(encoding.decode(chunk_tokens))
    return chunks


def embed_texts(client: OpenAI, model: str, texts: List[str]) -> List[List[float]]:
    """Embed a list of texts using OpenAI embeddings API."""
    embeddings: List[List[float]] = []
    for i in range(0, len(texts), 100):
        batch = texts[i : i + 100]
        resp = client.embeddings.create(model=model, input=batch)
        embeddings.extend([d.embedding for d in resp.data])
    return embeddings


def index_contracts(client: chromadb.PersistentClient, oai: OpenAI, model: str, file_path: Path) -> int:
    """Index contract chunks from a JSONL file."""
    collection = client.get_or_create_collection("contracts")
    ids: List[str] = []
    docs: List[str] = []
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            ids.append(str(item["chunk_id"]))
            docs.append(item["text"])
    if docs:
        embeddings = embed_texts(oai, model, docs)
        collection.upsert(ids=ids, documents=docs, embeddings=embeddings)
    return collection.count()


def index_authority(client: chromadb.PersistentClient, oai: OpenAI, model: str, kb_dir: Path) -> int:
    """Index authority documents located in kb_dir."""
    collection = client.get_or_create_collection("authority")
    if not kb_dir.exists():
        return collection.count()
    for path in sorted(kb_dir.iterdir()):
        if not path.is_file():
            continue
        text = read_text(path)
        if not text.strip():
            continue
        chunks = chunk_text(text)
        ids = [f"{path.stem}:{i}" for i in range(len(chunks))]
        metadatas = [{"source": str(path), "chunk": i} for i in range(len(chunks))]
        embeddings = embed_texts(oai, model, chunks)
        collection.upsert(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)
    return collection.count()


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Build Chroma index")
    parser.add_argument("--kb-dir", default=root / "data" / "kb", type=Path)
    parser.add_argument("--chunks-file", default=root / "data" / "chunks.jsonl", type=Path)
    parser.add_argument(
        "--model",
        default="text-embedding-3-small",
        choices=["text-embedding-3-small", "text-embedding-3-large"],
    )
    parser.add_argument("--persist-dir", default=Path(__file__).resolve().parent / "chroma", type=Path)
    args = parser.parse_args()

    chroma_client = chromadb.PersistentClient(path=str(args.persist_dir))
    oai = OpenAI()

    contracts_count = index_contracts(chroma_client, oai, args.model, args.chunks_file)
    authority_count = index_authority(chroma_client, oai, args.model, args.kb_dir)

    print(f"contracts collection: {contracts_count}")
    print(f"authority collection: {authority_count}")


if __name__ == "__main__":  # pragma: no cover
    main()
