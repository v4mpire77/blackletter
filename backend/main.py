from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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
@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    """Serve a simple landing page for the API."""
    return (
        "<!DOCTYPE html>"
        "<html>"
        "<head><title>Blackletter Systems</title></head>"
        "<body>"
        "<h1>Blackletter Systems API</h1>"
        "<p>The backend is running.</p>"
        "<p>See the <a href=\"/docs\">API docs</a>.</p>"
        "</body>"
        "</html>"
    )

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}
