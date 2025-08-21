from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from dotenv import load_dotenv

# ------- Robust router imports (works from different working dirs) -------
def _import_router(pkg_a: str, pkg_b: str):
    try:
        return __import__(pkg_a, fromlist=["router"])
    except Exception:
        return __import__(pkg_b, fromlist=["router"])

contracts = _import_router("backend.routers.contracts", "routers.contracts")
issues    = _import_router("backend.routers.issues",    "routers.issues")
coverage  = _import_router("backend.routers.coverage",  "routers.coverage")
redlines  = _import_router("backend.routers.redlines",  "routers.redlines")
gemini    = _import_router("backend.routers.gemini",    "routers.gemini")

# Load env (local/dev convenience)
load_dotenv()

app = FastAPI(title="Blackletter")

# ------- CORS -------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://blackletter.vercel.app",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------- Optional: serve exported Next.js UI from /app (frontend/out) -------
FRONTEND_BUILD_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../frontend/out")
)
if os.path.exists(FRONTEND_BUILD_DIR):
    app.mount("/app", StaticFiles(directory=FRONTEND_BUILD_DIR, html=True), name="app")

    @app.get("/")
    def root():
        return RedirectResponse("/app")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        index_path = os.path.join(FRONTEND_BUILD_DIR, "index.html")
        return FileResponse(index_path)

# ------- Health -------
@app.get("/health")
def health():
    return {"service": "blackletter", "status": "ok"}

# ------- API Routers -------
app.include_router(contracts.router, prefix="/api", tags=["contracts"])
app.include_router(issues.router,    prefix="/api", tags=["issues"])
app.include_router(coverage.router,  prefix="/api", tags=["coverage"])
app.include_router(redlines.router,  prefix="/api", tags=["redlines"])
app.include_router(gemini.router,    prefix="/api", tags=["gemini"])

# ------- Optional: mount RAG sub‑app if available -------
try:
    from rag.api import app as rag_app  # type: ignore
    app.mount("/rag", rag_app)
except Exception:
    pass

# ------- Optional: OCR router (guarded by ENABLE_OCR) -------
ENABLE_OCR = os.getenv("ENABLE_OCR", "false").lower() in {"1", "true", "yes"}
if ENABLE_OCR:
    try:
        try:
            from backend.routers import ocr as ocr_mod  # type: ignore
        except Exception:
            from routers import ocr as ocr_mod  # type: ignore
        app.include_router(ocr_mod.router, prefix="/api/ocr", tags=["ocr"])
    except Exception:
        # OCR deps not installed or router missing; ignore silently
        pass
