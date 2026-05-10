from __future__ import annotations

from flask import Blueprint

from services.api_response import success_response
from services.metrics_service import runtime_metrics


health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return success_response(
        {
            "status": "ok",
            **runtime_metrics.snapshot(),
        }
    )
