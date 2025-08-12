from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import contracts

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

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}
