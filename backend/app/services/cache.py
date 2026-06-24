import json
import logging
from typing import Any, Optional
from redis.asyncio import Redis, from_url

from app.core.config import settings

logger = logging.getLogger("cache_service")

class CacheService:
    def __init__(self):
        self.redis: Optional[Redis] = None
        self._in_memory_cache = {}

        if settings.USE_REDIS and settings.REDIS_URL:
            try:
                self.redis = from_url(settings.REDIS_URL, decode_responses=True)
                logger.info("Connected to Redis successfully.")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}. Falling back to in-memory cache.")
                self.redis = None

    async def get(self, key: str) -> Optional[Any]:
        if self.redis:
            try:
                data = await self.redis.get(key)
                if data:
                    return json.loads(data)
            except Exception as e:
                logger.error(f"Redis get error: {e}")
        
        # In-memory fallback
        return self._in_memory_cache.get(key)

    async def set(self, key: str, value: Any, expire_seconds: int = 86400) -> bool:
        if self.redis:
            try:
                await self.redis.set(key, json.dumps(value), ex=expire_seconds)
                return True
            except Exception as e:
                logger.error(f"Redis set error: {e}")
        
        # In-memory fallback
        self._in_memory_cache[key] = value
        # Basic expiration cleanup could be added if needed, but for fallback it's fine
        return True

    async def delete(self, key: str) -> bool:
        if self.redis:
            try:
                await self.redis.delete(key)
                return True
            except Exception as e:
                logger.error(f"Redis delete error: {e}")
        
        if key in self._in_memory_cache:
            del self._in_memory_cache[key]
            return True
        return False

cache_service = CacheService()
