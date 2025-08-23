"""FastAPI router exports for convenience.

This module collects the individual routers defined in this package and
re-exports them with stable names so that `backend.main` can include them
without importing each submodule separately.
"""

from .contracts import router as contracts_router
from .dashboard import router as dashboard_router
from .rag import router as rag_router
from .gemini import router as gemini_router
from .ocr import router as ocr_router

__all__ = [
    "contracts_router",
    "dashboard_router",
    "rag_router",
    "gemini_router",
    "ocr_router",
]
