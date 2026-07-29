"""
Redis asinxron kesh va rate-limiter mijozi.
"""

import os

import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def get_redis():

    return redis_client

async def close_redis():

    await redis_client.aclose()

