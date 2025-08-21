from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

from .routers import contracts, issues, coverage, redlines, gemini
# from .routers import ocr_example  # optional OCR example
# from .routers import llm_test  # optional

load_dotenv()  # only needed locally

app = FastAPI(title="Blackletter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your frontend origin later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"service": "blackletter", "status": "ok"}

app.include_router(contracts.router, prefix="/api", tags=["contracts"])
app.include_router(issues.router,    prefix="/api", tags=["issues"])
app.include_router(coverage.router,  prefix="/api", tags=["coverage"])
app.include_router(redlines.router,  prefix="/api", tags=["redlines"])
# Gemini endpoint for prompt testing
app.include_router(gemini.router,    prefix="/api", tags=["gemini"])
# OCR example endpoint (optional) - uncomment the import and this line to enable
# app.include_router(ocr_example.router, prefix="/api", tags=["ocr"])
# app.include_router(llm_test.router,  prefix="/api", tags=["llm"])

FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(__file__), "../frontend/out")

if os.path.exists(FRONTEND_BUILD_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_BUILD_DIR, html=True), name="frontend")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        index_path = os.path.join(FRONTEND_BUILD_DIR, "index.html")
        return FileResponse(index_path)
