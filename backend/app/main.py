from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
import logging

from app.core.config import settings
from app.api.v1.api import api_router
from app.api.middleware.rate_limit import RateLimitMiddleware
from app.services.cache import cache_service
from app.services.google_maps import google_maps_service

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Tourist Discovery API...")
    yield
    # Shutdown
    logger.info("Shutting down Tourist Discovery API...")
    if cache_service.redis:
        await cache_service.redis.close()
        logger.info("Closed Redis connections.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Rate Limiting Middleware
app.add_middleware(RateLimitMiddleware)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API endpoints router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint to verify API and dependencies are running."""
    db_status = "healthy"
    cache_status = "healthy"
    
    if cache_service.redis:
        try:
            await cache_service.redis.ping()
        except Exception:
            cache_status = "unhealthy"
            
    return {
        "status": "online",
        "database": db_status,
        "cache": cache_status,
        "mock_mode": google_maps_service.is_mock_mode
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "A critical system error occurred. Please try again later."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
