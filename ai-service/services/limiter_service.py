from __future__ import annotations

import logging
import os

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


logger = logging.getLogger(__name__)


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30 per minute"],
)


def _redis_is_available(redis_url: str) -> bool:
    try:
        import redis

        client = redis.Redis.from_url(
            redis_url,
            socket_connect_timeout=1,
            socket_timeout=1,
        )
        client.ping()
        return True
    except Exception as exc:
        logger.warning(
            "limiter_redis_unavailable storage_uri=%s exception_type=%s",
            redis_url,
            type(exc).__name__,
        )
        return False


def configure_limiter(app: Flask) -> None:
    storage_uri = os.getenv("RATE_LIMIT_STORAGE_URI") or os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0",
    )

    if storage_uri.startswith("redis://") or storage_uri.startswith("rediss://"):
        if _redis_is_available(storage_uri):
            app.config["RATELIMIT_STORAGE_URI"] = storage_uri
            logger.info("limiter_storage_initialized backend=redis storage_uri=%s", storage_uri)
        else:
            app.config["RATELIMIT_STORAGE_URI"] = "memory://"
            logger.warning("limiter_storage_fallback backend=memory reason=redis_unavailable")
    else:
        app.config["RATELIMIT_STORAGE_URI"] = storage_uri
        logger.info("limiter_storage_initialized backend=%s", storage_uri)

    limiter.init_app(app)
