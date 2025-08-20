from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import contracts, dashboard

app = FastAPI(title="Blackletter Systems API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://blackletter.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(contracts.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}
