from __future__ import annotations

import hashlib
import json
import logging
import os
from typing import Any


logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 15 * 60


def build_cache_key(namespace: str, payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return f"ai-service:{namespace}:{digest}"


class RedisCache:
    def __init__(self) -> None:
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.enabled = os.getenv("REDIS_CACHE_ENABLED", "true").lower() == "true"
        self._client = None

    def _get_client(self):
        if not self.enabled:
            return None

        if self._client is None:
            try:
                import redis

                self._client = redis.Redis.from_url(
                    self.redis_url,
                    decode_responses=True,
                    socket_connect_timeout=0.2,
                    socket_timeout=0.2,
                )
            except Exception:
                logger.exception("Redis client initialization failed")
                self.enabled = False
                return None

        return self._client

    def get(self, key: str) -> Any | None:
        client = self._get_client()
        if client is None:
            return None

        try:
            cached = client.get(key)
            if not cached:
                logger.info("cache_miss key=%s", key)
                return None
            logger.info("cache_hit key=%s", key)
            return json.loads(cached)
        except Exception:
            logger.exception("Redis cache read failed")
            return None

    def set(self, key: str, value: Any, ttl_seconds: int = CACHE_TTL_SECONDS) -> None:
        client = self._get_client()
        if client is None:
            return

        try:
            client.setex(key, ttl_seconds, json.dumps(value, separators=(",", ":")))
            logger.info("cache_write key=%s ttl_seconds=%s", key, ttl_seconds)
        except Exception:
            logger.exception("Redis cache write failed")


redis_cache = RedisCache()
