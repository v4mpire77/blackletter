from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Try to import the contracts router from the package; fall back to top-level if needed
try:
    from backend.routers import contracts
except Exception:
    # when running tests or in different working dir the plain import may work
    from routers import contracts


app = FastAPI(title="Blackletter Systems API")

# Configure CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers (safe-guard if router missing)
try:
    app.include_router(contracts.router, prefix="/api")
except Exception:
    # If the contracts router isn't available, continue with basic health endpoint
    pass

# Try to mount the RAG app (serve RAG endpoints under /rag) if available
try:
    # rag.api should expose a FastAPI instance named `app`
    from rag.api import app as rag_app

    app.mount("/rag", rag_app)
except Exception:
    # rag not present or import failed; skip mounting
    pass


@app.get("/health")
async def health_check():
    return {"status": "ok"}
