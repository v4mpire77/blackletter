from __future__ import annotations
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from dotenv import load_dotenv

# Import routers with error handling
try:
    from .routers import contracts, dashboard, rag, nlp_router, gemini
except ImportError:
    # Fallback for basic functionality
    from .routers import contracts, gemini

load_dotenv()  # only needed locally

app = FastAPI(title="Blackletter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://blackletter-frontend.onrender.com",
        "https://blackletter-systems.onrender.com",
        "https://blackletter.vercel.app",
        "*",  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the frontend build directory
FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(__file__), "../frontend/out")

# Mount the frontend static files if the directory exists
if os.path.exists(FRONTEND_BUILD_DIR):
    # Mount the main frontend assets under /app/
    app.mount("/app", StaticFiles(directory=FRONTEND_BUILD_DIR, html=True), name="app")

    # Send root to the UI at /app/
    @app.get("/")
    def root():
        return RedirectResponse("/app")

    # Serve frontend for all other paths if it's mounted, for client-side routing
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # This is a fallback for client-side routing,
        # ensuring all unmatched paths serve the index.html
        index_path = os.path.join(FRONTEND_BUILD_DIR, "index.html")
        return FileResponse(index_path)

# Health check endpoint
@app.get("/health")
def health():
    return {"service": "blackletter", "status": "ok"}

# API Routers - Mount with error handling
app.include_router(contracts.router, prefix="/api", tags=["contracts"])
app.include_router(gemini.router, prefix="/api", tags=["gemini"])

# Optional routers - mount if available
try:
    app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])
except NameError:
    print("Dashboard router not available")

try:
    app.include_router(rag.router, prefix="/api/rag", tags=["rag"])
except NameError:
    print("RAG router not available")

try:
    app.include_router(nlp_router.router, prefix="/api", tags=["nlp"])
except NameError:
    print("NLP router not available")

# OCR router - conditionally mounted when ENABLE_OCR=true
ENABLE_OCR = os.getenv("ENABLE_OCR", "false").lower() in {"1", "true", "yes"}
if ENABLE_OCR:
    try:
        from .routers import ocr
        app.include_router(ocr.router, prefix="/api/ocr", tags=["ocr"])
    except ImportError:
        print("OCR dependencies not available - OCR functionality will be disabled")

# Optional: mount RAG sub-app if available
try:
    from rag.api import app as rag_app  # type: ignore
    app.mount("/rag", rag_app)
except Exception:
    pass