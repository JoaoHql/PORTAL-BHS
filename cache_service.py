# cache_service.py

import asyncio
import redis.asyncio as redis
from typing import Any, Optional

# Configuração do Redis
REDIS_URL = "redis://localhost:6379"

class CacheService:
    def __init__(self, redis_url: str = REDIS_URL):
        self.redis_url = redis_url
        self.redis = redis.from_url(self.redis_url, decode_responses=True)

    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        await self.redis.close()


# Example usage (for testing purposes)
#async def teste_cache():
#    cache = CacheService()
#    await cache.set("msg", "olá mundo", expire=10)
#    print(await cache.get("msg"))
#    await cache.delete("msg")
#    await cache.close()
#if __name__ == "__main__":
#    asyncio.run(teste_cache())