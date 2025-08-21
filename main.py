from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.routers import contracts, issues, coverage, redlines
# from backend.routers import llm_test  # optional

app = FastAPI(title="Blackletter")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
# app.include_router(llm_test.router,  prefix="/api", tags=["llm"])

FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(__file__), "frontend/out")

if os.path.exists(FRONTEND_BUILD_DIR):
    # Mount the Next.js static assets
    static_dir = os.path.join(FRONTEND_BUILD_DIR, "_next/static")
    if os.path.exists(static_dir):
        app.mount("/_next/static", StaticFiles(directory=static_dir), name="nextjs_static")
    
    # Catch-all route for SPA - this should be last to avoid interfering with API routes
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Don't serve index.html for API routes
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")
        
        # For Next.js assets, serve them directly from the build directory
        if full_path.startswith("_next/"):
            file_path = os.path.join(FRONTEND_BUILD_DIR, full_path)
            if os.path.exists(file_path):
                return FileResponse(file_path)
        
        # For all other routes, serve the index.html (SPA routing)
        index_path = os.path.join(FRONTEND_BUILD_DIR, "index.html")
        return FileResponse(index_path)