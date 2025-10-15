"""
Main FastAPI application for autocash-ultimate.

Privacy-first, LGPD-compliant content generation and monetization platform.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time

from app.config import settings
from app.db import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Privacy-first autonomous content generation and monetization platform",
    docs_url="/docs" if settings.DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    if settings.ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Kill switch middleware
@app.middleware("http")
async def kill_switch_check(request: Request, call_next):
    """Check kill switch before processing requests."""
    if settings.KILL_SWITCH_ENABLED:
        # Check if request is for admin/monitoring endpoints
        if not request.url.path.startswith("/health") and not request.url.path.startswith("/admin"):
            return JSONResponse(
                status_code=503,
                content={
                    "error": "Service temporarily paused",
                    "message": "Content generation is currently paused. Contact admin."
                }
            )
    
    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Validate settings
    try:
        settings.validate()
        logger.info("Settings validated successfully")
    except ValueError as e:
        logger.error(f"Settings validation failed: {e}")
        if settings.ENVIRONMENT == "production":
            raise
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Application shutting down")


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "review_required": settings.REVIEW_REQUIRED,
        "docs": "/docs" if settings.DEBUG else "disabled",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "kill_switch": settings.KILL_SWITCH_ENABLED,
    }


# Import and include routers
from app.routes import generate, metrics, tracking, privacy, admin, batch_generate, publisher, repurposer

app.include_router(generate.router, prefix="/api", tags=["content"])
app.include_router(metrics.router, prefix="/api", tags=["monitoring"])
app.include_router(tracking.router, prefix="/api/tracking", tags=["tracking"])
app.include_router(privacy.router, prefix="/api/privacy", tags=["privacy"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(batch_generate.router, prefix="/api", tags=["batch"])
app.include_router(publisher.router, prefix="/api", tags=["publisher"])
app.include_router(repurposer.router, prefix="/api", tags=["repurposer"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
