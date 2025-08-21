from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "out")
if os.path.isdir(FRONTEND_BUILD_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_BUILD_DIR, html=True), name="frontend")

# include your routers under /api to avoid clashing with static files
# app.include_router(api_router, prefix="/api")
