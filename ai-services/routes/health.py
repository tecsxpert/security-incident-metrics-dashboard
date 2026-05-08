# ai-service/routes/health.py

import os
import time
import logging
from flask import Blueprint, jsonify

logger    = logging.getLogger(__name__)
health_bp = Blueprint("health_bp", __name__)

START_TIME     = time.time()
response_times = []
MAX_TRACKED    = 100


def record_response_time(elapsed: float):
    response_times.append(elapsed)
    if len(response_times) > MAX_TRACKED:
        response_times.pop(0)


def get_avg_response_time() -> float:
    if not response_times:
        return 0.0
    return round(sum(response_times) / len(response_times), 3)


def get_uptime() -> dict:
    elapsed = int(time.time() - START_TIME)
    return {
        "days":          elapsed // 86400,
        "hours":         (elapsed % 86400) // 3600,
        "minutes":       (elapsed % 3600) // 60,
        "seconds":       elapsed % 60,
        "total_seconds": elapsed
    }


@health_bp.route("/health", methods=["GET"])
def health():
    from services.cache_service import cache
    logger.info("Health check called")
    return jsonify({
        "status":            "ok",
        "service":           "ai-service",
        "port":              5000,
        "model":             os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
        "avg_response_time": get_avg_response_time(),
        "uptime":            get_uptime(),
        "cache_enabled":     cache.enabled
    }), 200