from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import contracts, dashboard, rag, nlp_router

app = FastAPI(title="Blackletter Systems API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://blackletter-frontend.onrender.com",
        "https://blackletter-systems.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(contracts.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(rag.router, prefix="/api/rag")
app.include_router(nlp_router.router, prefix="/api")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}
