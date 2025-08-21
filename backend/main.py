from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import os

from .routers import contracts, issues, coverage, redlines
# from .routers import llm_test  # optional

app = FastAPI(title="Blackletter Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your frontend origin later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Mount the exported Next.js site at /app if it exists
if os.path.isdir("frontend/out"):
    app.mount("/app", StaticFiles(directory="frontend/out", html=True), name="app")

# Send root to the UI (docs still available at /docs)
@app.get("/")
def root():
    return RedirectResponse(url="/app")

app.include_router(contracts.router, prefix="/api", tags=["contracts"])
app.include_router(issues.router,    prefix="/api", tags=["issues"])
app.include_router(coverage.router,  prefix="/api", tags=["coverage"])
app.include_router(redlines.router,  prefix="/api", tags=["redlines"])
# app.include_router(llm_test.router,  prefix="/api", tags=["llm"])
