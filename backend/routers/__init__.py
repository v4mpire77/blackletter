"""FastAPI router exports for convenience.

This module collects the individual routers defined in this package and
re-exports them with stable names so that `backend.main` can include them
without importing each submodule separately.
"""

from . import contracts, gemini, rag

try:  # Dashboard router is optional
    from . import dashboard  # type: ignore
except ImportError:  # pragma: no cover - dashboard not available
    dashboard = None  # type: ignore

try:  # OCR router is optional
    from . import ocr  # type: ignore
except ImportError:  # pragma: no cover - OCR not available
    ocr = None  # type: ignore

# Re-export router objects with stable names
contracts_router = contracts.router
rag_router = rag.router
gemini_router = gemini.router

dashboard_router = dashboard.router if dashboard else None  # type: ignore
ocr_router = ocr.router if ocr else None  # type: ignore

__all__ = [
    "contracts",
    "rag",
    "gemini",
    "contracts_router",
    "rag_router",
    "gemini_router",
]

if dashboard_router:
    __all__.extend(["dashboard", "dashboard_router"])

if ocr_router:
    __all__.extend(["ocr", "ocr_router"])
