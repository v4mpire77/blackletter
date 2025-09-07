from fastapi import FastAPI

from backend.core.config import settings
from backend.routers import jobs

app = FastAPI(
    title=settings.APP_NAME,
    description="API for submitting and tracking contract analysis jobs.",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


@app.get("/", tags=["Health Check"])
async def root() -> dict[str, str]:
    return {"status": "ok", "message": f"Welcome to the {settings.APP_NAME}"}


app.include_router(jobs.router, prefix=f"{settings.API_V1_STR}/jobs", tags=["Jobs"])
