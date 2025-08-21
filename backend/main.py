from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from .routers import contracts, dashboard

app = FastAPI(title="Blackletter Systems API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(contracts.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

# Root route redirects to API docs
@app.get("/")
async def root():
    """Redirect to interactive API documentation."""
    return RedirectResponse(url="/docs")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}
