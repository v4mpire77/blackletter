from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .routers import contracts, issues, coverage, redlines
# from .routers import llm_test  # optional

app = FastAPI(title="Blackletter Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Serve the exported Next.js site
app.mount("/app", StaticFiles(directory="frontend/out", html=True), name="app")

# Send root to the UI
@app.get("/")
def root():
    return RedirectResponse("/app")

app.include_router(contracts.router, prefix="/api", tags=["contracts"])
app.include_router(issues.router,    prefix="/api", tags=["issues"])
app.include_router(coverage.router,  prefix="/api", tags=["coverage"])
app.include_router(redlines.router,  prefix="/api", tags=["redlines"])
# app.include_router(llm_test.router,  prefix="/api", tags=["llm"])
