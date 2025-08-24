from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import review

app = FastAPI(title="Blackletter Review API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review.router, prefix="/api")

@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}
