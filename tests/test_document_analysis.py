import os
import sys
from typing import List
from unittest.mock import patch

# Ensure project root is on path for "src" package
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.backend.services.document_analysis import DocumentAnalyzer


class StubPage:
    width = 100
    height = 100
    images = [{"x0": 10, "top": 10, "x1": 20, "bottom": 20}]

    def extract_text(self) -> str:
        return "HEADER\nClause 1: Hello"

    def extract_words(self, use_text_flow: bool = True) -> List[dict]:
        return [
            {"text": "HEADER", "x0": 0, "x1": 50, "top": 0, "bottom": 10},
            {"text": "Clause", "x0": 0, "x1": 40, "top": 20, "bottom": 30},
            {"text": "1:", "x0": 41, "x1": 44, "top": 20, "bottom": 30},
            {"text": "Hello", "x0": 45, "x1": 80, "top": 20, "bottom": 30},
        ]

    def extract_tables(self) -> List[List[List[str]]]:
        return [[["A", "B"], ["1", "2"]]]


class StubPDF:
    def __init__(self) -> None:
        self.pages = [StubPage()]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def test_document_analyzer_extracts_elements() -> None:
    with patch("src.backend.services.document_analysis.pdfplumber.open", return_value=StubPDF()):
        analyzer = DocumentAnalyzer()
        doc = analyzer.analyze(b"pdf")

    types = {e.type for e in doc.elements}
    assert {"header", "text", "table", "image"}.issubset(types)
    text_elem = next(e for e in doc.elements if e.type == "text" and e.text.startswith("Clause"))
    assert text_elem.bbox is not None
