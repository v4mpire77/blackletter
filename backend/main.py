from __future__ import annotations
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv
import time
import logging

# Import routers with error handling
try:
    from .routers import contracts, rag, gemini
except ImportError:
    # Fallback for basic functionality
    from .routers import contracts, gemini

load_dotenv()  # only needed locally

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Blackletter Systems",
    description="AI-powered legal document analysis platform",
    version="1.0.0",
    docs_url="/docs" if not security_config.is_production() else None,
    redoc_url="/redoc" if not security_config.is_production() else None,
)

# Security: Trusted Host middleware
if security_config.is_production():
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=security_config.get_trusted_hosts()
    )

# Import security configuration
from .app.core.security_config import security_config

# Security: Environment-based CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=security_config.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Define the frontend build directory
FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(__file__), "../frontend/out")

# Mount the frontend static files if the directory exists
if os.path.exists(FRONTEND_BUILD_DIR):
    # Mount the main frontend assets under /app/
    app.mount("/app", StaticFiles(directory=FRONTEND_BUILD_DIR, html=True), name="app")

    # Send root to the UI at /app/
    @app.get("/")
    def root():
        return RedirectResponse("/app")

    # Serve frontend for all other paths if it's mounted, for client-side routing
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # This is a fallback for client-side routing,
        # ensuring all unmatched paths serve the index.html
        index_path = os.path.join(FRONTEND_BUILD_DIR, "index.html")
        return FileResponse(index_path)

# Security: Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors without exposing internal details"""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request data", "type": "validation_error"}
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with sanitized responses"""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "http_error"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions without exposing system details"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "server_error"}
    )

# Security: Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add request timing and security headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Security headers from configuration
    security_headers = security_config.get_security_headers()
    for header, value in security_headers.items():
        response.headers[header] = value
    
    # Performance headers
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Health check endpoint
@app.get("/health")
def health():
    return {"service": "blackletter", "status": "ok", "environment": security_config.ENVIRONMENT}

# API Routers - Mount with error handling
app.include_router(contracts.router, prefix="/api", tags=["contracts"])
app.include_router(gemini.router, prefix="/api", tags=["gemini"])

# Optional routers - mount if available
# Dashboard router not available

try:
    app.include_router(rag.router, prefix="/api/rag", tags=["rag"])
except NameError:
    print("RAG router not available")

# NLP router not available

# OCR router - conditionally mounted when ENABLE_OCR=true
ENABLE_OCR = os.getenv("ENABLE_OCR", "false").lower() in {"1", "true", "yes"}
if ENABLE_OCR:
    try:
        from .routers import ocr
        app.include_router(ocr.router, prefix="/api/ocr", tags=["ocr"])
    except ImportError:
        print("OCR dependencies not available - OCR functionality will be disabled")

# Optional: mount RAG sub-app if available
try:
    from rag.api import app as rag_app  # type: ignore
    app.mount("/rag", rag_app)
except Exception:
    pass