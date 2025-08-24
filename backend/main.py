from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .routers import contracts, dashboard, jobs

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
app.include_router(
    jobs.router, prefix=f"/api/{settings.API_VERSION}/jobs", tags=["Jobs"]
)


# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}
