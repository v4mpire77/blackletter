from __future__ import annotations

"""Multi-modal document analysis utilities.

This module builds on top of the existing OCR and NLP tooling to
extract text, tables, images and rudimentary document structure from
PDF files.  It produces a unified representation that keeps spatial
information for downstream tasks such as RAG indexing.

The implementation purposely keeps external dependencies optional so
that the rest of the application can run even when PDF/OCR libraries
are not installed.  When the required libraries are missing a
``RuntimeError`` is raised with a helpful message.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import io

# OCR service from the existing module
from .ocr import ocr_available

# ``NLPEngine`` is heavy to initialise; we only import the type for
# static checking and instantiate lazily when provided by callers.
try:  # pragma: no cover - optional dependency
    from backend.app.core.nlp_engine import NLPEngine  # type: ignore
except Exception:  # pragma: no cover - handled gracefully
    NLPEngine = None  # type: ignore

# Optional dependency: pdfplumber for layout analysis
try:  # pragma: no cover - optional dependency
    import pdfplumber  # type: ignore
except Exception:  # pragma: no cover - handled gracefully
    pdfplumber = None  # type: ignore

# Optional dependency: pytesseract for OCR fallbacks
try:  # pragma: no cover - optional dependency
    import pytesseract  # type: ignore
    from PIL import Image  # type: ignore
except Exception:  # pragma: no cover - handled gracefully
    pytesseract = None  # type: ignore
    Image = None  # type: ignore


@dataclass
class DocumentElement:
    """Represents a single piece of a document.

    Attributes:
        type: Type of the element (e.g. ``text``, ``table``, ``image``,
            ``header``).
        text: Extracted textual content, if any.
        bbox: Bounding box ``(x0, top, x1, bottom)`` in PDF coordinates.
        page: Page number starting from ``1``.
        extra: Arbitrary extra metadata.
    """

    type: str
    text: Optional[str] = None
    bbox: Optional[Tuple[float, float, float, float]] = None
    page: int = 0
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Document:
    """Unified representation of a PDF document."""

    elements: List[DocumentElement] = field(default_factory=list)


class DocumentAnalyzer:
    """High level multi-modal PDF processor."""

    def __init__(self, nlp_engine: Optional["NLPEngine"] = None) -> None:
        self.nlp = nlp_engine

    # ------------------------------------------------------------------
    # public API
    # ------------------------------------------------------------------
    def analyze(self, pdf_bytes: bytes) -> Document:
        """Analyse a PDF and return a :class:`Document`.

        Args:
            pdf_bytes: Raw bytes of the PDF file.
        """
        if pdfplumber is None:  # pragma: no cover - import guard
            raise RuntimeError(
                "pdfplumber is required for document analysis."
            )

        elements: List[DocumentElement] = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                elements.extend(self._extract_page_elements(page, page_num))

        return Document(elements=elements)

    def to_rag_chunks(self, document: Document) -> List[str]:
        """Convert :class:`Document` into text chunks for RAG indexing."""
        return [elem.text for elem in document.elements if elem.text]

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def _extract_page_elements(self, page: "pdfplumber.page.Page", page_num: int) -> List[DocumentElement]:  # type: ignore[name-defined]
        elems: List[DocumentElement] = []

        # --- text & structural elements ---
        text = page.extract_text() or ""
        if text.strip():
            # Use word-level boxes to preserve spatial layout
            try:
                words = page.extract_words(use_text_flow=True)
            except Exception:  # pragma: no cover - pdfplumber internal errors
                words = []

            lines = self._group_words_by_line(words)
            for line_words in lines:
                line_text = " ".join(w["text"] for w in line_words).strip()
                x0 = min(float(w["x0"]) for w in line_words)
                x1 = max(float(w["x1"]) for w in line_words)
                top = min(float(w["top"]) for w in line_words)
                bottom = max(float(w["bottom"]) for w in line_words)
                elem_type = "header" if self._is_heading(line_text) else "text"
                elems.append(
                    DocumentElement(
                        type=elem_type,
                        text=line_text,
                        bbox=(x0, top, x1, bottom),
                        page=page_num,
                    )
                )
        else:
            # OCR fallback for image-based pages
            if ocr_available() and pytesseract and Image:  # pragma: no cover - requires OCR deps
                img = page.to_image(resolution=150)
                pil = img.original.convert("RGB")
                ocr_text = pytesseract.image_to_string(pil) or ""
                elems.append(
                    DocumentElement(
                        type="text",
                        text=ocr_text.strip(),
                        bbox=(0, 0, float(page.width), float(page.height)),
                        page=page_num,
                    )
                )

        # --- tables ---
        try:
            tables = page.extract_tables()
        except Exception:  # pragma: no cover - pdfplumber internal errors
            tables = []
        for table in tables:
            table_text = "\n".join("\t".join(cell or "" for cell in row) for row in table)
            elems.append(
                DocumentElement(
                    type="table",
                    text=table_text,
                    bbox=None,
                    page=page_num,
                )
            )

        # --- images/diagrams ---
        for img in getattr(page, "images", []):
            bbox = (
                float(img.get("x0", 0)),
                float(img.get("top", 0)),
                float(img.get("x1", 0)),
                float(img.get("bottom", 0)),
            )
            elems.append(
                DocumentElement(
                    type="image",
                    text=None,
                    bbox=bbox,
                    page=page_num,
                )
            )

        return elems

    def _group_words_by_line(self, words: List[Dict[str, Any]], tolerance: float = 2.0) -> List[List[Dict[str, Any]]]:
        """Group word boxes into lines.

        pdfplumber returns word boxes with ``top`` and ``bottom``
        coordinates.  Words whose vertical positions are within
        ``tolerance`` pixels are considered part of the same line.
        """
        if not words:
            return []

        words = sorted(words, key=lambda w: (w["top"], w["x0"]))
        lines: List[List[Dict[str, Any]]] = []
        current: List[Dict[str, Any]] = []
        last_top: Optional[float] = None

        for w in words:
            top = float(w["top"])
            if last_top is None or abs(top - last_top) <= tolerance:
                current.append(w)
            else:
                lines.append(current)
                current = [w]
            last_top = top

        if current:
            lines.append(current)
        return lines

    def _is_heading(self, text: str) -> bool:
        """Heuristic heading/section detection."""
        stripped = text.strip()
        if not stripped:
            return False
        if stripped.isupper():
            return True
        lowered = stripped.lower()
        if lowered.startswith(("section", "clause", "article")) and stripped.endswith(":"):
            return True
        if stripped[0].isdigit() and stripped.endswith(":"):
            return True
        return False


__all__ = ["Document", "DocumentElement", "DocumentAnalyzer"]
