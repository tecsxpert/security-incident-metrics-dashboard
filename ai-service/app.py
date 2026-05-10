from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from time import time

from dotenv import load_dotenv
from flask import Flask, jsonify, g, request
from flask_cors import CORS

load_dotenv()

from routes import register_blueprints
from services.error_handlers import register_error_handlers
from services.knowledge_service import initialize_ai_knowledge
from services.limiter_service import configure_limiter
from services.request_logging import register_request_logging
from services.security_middleware import register_security_middleware


SERVICE_START_TIME = time()
REQUEST_COUNT = 0
TOTAL_RESPONSE_TIME_MS = 0.0


def configure_logging() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def create_app() -> Flask:
    global REQUEST_COUNT
    global TOTAL_RESPONSE_TIME_MS

    configure_logging()

    app = Flask(__name__)

    CORS(app)

    configure_limiter(app)

    register_security_middleware(app)
    register_request_logging(app)
    register_error_handlers(app)

    @app.before_request
    def before_request():
        g.start_time = time()

        app.logger.info(
            "request_started method=%s path=%s remote_addr=%s",
            request.method,
            request.path,
            request.remote_addr,
        )

    @app.after_request
    def after_request(response):
        global REQUEST_COUNT
        global TOTAL_RESPONSE_TIME_MS

        start_time_value = getattr(g, "start_time", None)

        if start_time_value is not None:
            duration_ms = (time() - start_time_value) * 1000

            REQUEST_COUNT += 1
            TOTAL_RESPONSE_TIME_MS += duration_ms

            app.logger.info(
                "request_completed method=%s path=%s status=%s duration_ms=%.2f",
                request.method,
                request.path,
                response.status_code,
                duration_ms,
            )

        return response

    register_blueprints(app)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "service": "AI Service",
            "status": "running",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "describe": "/describe",
                "recommend": "/recommend",
                "generate_report": "/generate-report",
            },
        })

    @app.route("/health", methods=["GET"])
    def health():
        uptime_seconds = round(time() - SERVICE_START_TIME, 3)

        avg_response_time_ms = (
            round(TOTAL_RESPONSE_TIME_MS / REQUEST_COUNT, 3)
            if REQUEST_COUNT > 0
            else 0
        )

        return jsonify({
            "success": True,
            "data": {
                "status": "ok",
                "model_name": "llama-3.3-70b-versatile",
                "uptime_seconds": uptime_seconds,
                "request_count": REQUEST_COUNT,
                "avg_response_time_ms": avg_response_time_ms,
            },
            "error": None,
            "meta": {
                "generated_at": datetime.now(timezone.utc).isoformat()
            },
        })

    app.logger.info("Security Incident AI service initialized")

    initialize_ai_knowledge()

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
    )