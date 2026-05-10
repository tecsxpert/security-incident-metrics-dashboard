from __future__ import annotations

import time

from flask import Flask, g, request

from services.metrics_service import runtime_metrics


def register_request_logging(app: Flask) -> None:
    @app.before_request
    def log_request_start() -> None:
        g.request_started_at = time.perf_counter()
        app.logger.info(
            "request_started method=%s path=%s remote_addr=%s",
            request.method,
            request.path,
            request.headers.get("X-Forwarded-For", request.remote_addr),
        )

    @app.after_request
    def log_request_end(response):
        duration_ms = (time.perf_counter() - g.get("request_started_at", time.perf_counter())) * 1000
        runtime_metrics.record_response_time(duration_ms)
        response.headers["Content-Type"] = "application/json"
        app.logger.info(
            "request_completed method=%s path=%s status=%s duration_ms=%.2f",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
        )
        return response
