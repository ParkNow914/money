"""
FastAPI application entry point.
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from app.config import settings
from app.db import close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    print("🚀 Starting AutoCash Ultimate...")
    print(f"📊 Environment: {settings.environment}")
    print(f"🔐 Review Required: {settings.review_required}")

    # Initialize database
    await init_db()
    print("✅ Database initialized")

    # Check kill-switch
    if settings.killswitch_enabled:
        killswitch_path = Path(settings.killswitch_file)
        if killswitch_path.exists():
            print("🔴 KILL-SWITCH ACTIVE - Automated operations paused")
        else:
            print("✅ Kill-switch ready (not active)")

    yield

    # Shutdown
    print("👋 Shutting down AutoCash Ultimate...")
    await close_db()
    print("✅ Database connections closed")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Privacy-first, ethical content monetization ecosystem",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    killswitch_active = False
    if settings.killswitch_enabled:
        killswitch_path = Path(settings.killswitch_file)
        killswitch_active = killswitch_path.exists()

    return {
        "status": "healthy",
        "killswitch_active": killswitch_active,
        "review_required": settings.review_required,
        "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    if not settings.prometheus_enabled:
        return JSONResponse({"error": "Metrics disabled"}, status_code=404)

    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An error occurred",
            "path": str(request.url),
        },
    )


# Future routes will be added here
# from app.routes import generate, tracking, admin, privacy
# app.include_router(generate.router, prefix="/api/generate", tags=["generate"])
# app.include_router(tracking.router, prefix="/api/tracking", tags=["tracking"])
# app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
# app.include_router(privacy.router, prefix="/api/privacy", tags=["privacy"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
