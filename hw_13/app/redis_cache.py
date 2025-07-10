import json
import os
from redis.asyncio import Redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

class RedisCache:
    def __init__(self):
        self.redis: Redis = Redis.from_url(REDIS_URL, decode_responses=True)

    async def connect(self):
        # redis-py не требует явного подключения, но можно проверить ping
        try:
            await self.redis.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}")

    async def disconnect(self):
        await self.redis.close()

    async def get(self, key: str):
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def set(self, key: str, value, expire: int = 300):
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def delete_pattern(self, pattern: str):
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)

redis_cache = RedisCache()
