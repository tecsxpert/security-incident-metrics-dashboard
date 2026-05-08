# ai-service/services/cache_service.py

import os
import json
import hashlib
import logging
import redis

logger    = logging.getLogger(__name__)
CACHE_TTL = int(os.environ.get("AI_CACHE_TTL_SECONDS", 900))


class CacheService:

    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=os.environ.get("REDIS_HOST", "localhost"),
                port=int(os.environ.get("REDIS_PORT", 6379)),
                password=os.environ.get("REDIS_PASSWORD", None) or None,
                decode_responses=True,
                socket_connect_timeout=2,
            )
            self.redis.ping()
            self.enabled = True
            logger.info("CacheService connected to Redis successfully")
        except Exception as e:
            self.enabled = False
            logger.warning(f"CacheService — Redis unavailable, caching disabled: {str(e)}")

    def _make_key(self, endpoint: str, data: dict) -> str:
        raw = f"{endpoint}:{json.dumps(data, sort_keys=True)}"
        return "ai_cache:" + hashlib.sha256(raw.encode()).hexdigest()

    def get(self, endpoint: str, data: dict):
        if not self.enabled:
            return None
        try:
            cached = self.redis.get(self._make_key(endpoint, data))
            if cached:
                logger.info(f"Cache HIT — endpoint: {endpoint}")
                return json.loads(cached)
            logger.info(f"Cache MISS — endpoint: {endpoint}")
            return None
        except Exception as e:
            logger.warning(f"Cache GET error — {str(e)}")
            return None

    def set(self, endpoint: str, data: dict, response: dict) -> bool:
        if not self.enabled:
            return False
        try:
            self.redis.setex(self._make_key(endpoint, data), CACHE_TTL, json.dumps(response))
            logger.info(f"Cache SET — endpoint: {endpoint} TTL: {CACHE_TTL}s")
            return True
        except Exception as e:
            logger.warning(f"Cache SET error — {str(e)}")
            return False


cache = CacheService()