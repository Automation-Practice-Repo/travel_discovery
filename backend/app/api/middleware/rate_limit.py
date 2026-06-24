import time
from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import settings
from app.services.cache import cache_service

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Bypass rate limiting for endpoints other than API or for OPTIONS preflight
        if not request.url.path.startswith(settings.API_V1_STR) or request.method == "OPTIONS":
            return await call_next(request)

        # Get client IP
        client_ip = request.client.host if request.client else "unknown_ip"
        
        # Define current minute window bucket
        current_minute = int(time.time() // settings.RATE_LIMIT_WINDOW)
        cache_key = f"rate_limit:{client_ip}:{current_minute}"

        # Get current count
        count = await cache_service.get(cache_key)
        
        if count is None:
            # First request in this window
            await cache_service.set(cache_key, 1, expire_seconds=settings.RATE_LIMIT_WINDOW)
            count = 1
        else:
            count = int(count)

        if count > settings.RATE_LIMIT_LIMIT:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Rate limit exceeded. Please wait before searching again."
                }
            )

        # Increment count
        await cache_service.set(cache_key, count + 1, expire_seconds=settings.RATE_LIMIT_WINDOW)

        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_LIMIT)
        response.headers["X-RateLimit-Remaining"] = str(max(0, settings.RATE_LIMIT_LIMIT - count))
        
        return response
