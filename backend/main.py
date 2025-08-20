from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import contracts, dashboard

app = FastAPI(title="Blackletter Systems API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(contracts.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

# Root route for basic status check
@app.get("/")
async def root():
    """Root endpoint returning a simple status message."""
    return {"status": "Blackletter Systems API running"}

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}
