from __future__ import annotations

from flask import Flask, current_app, request
from flask_limiter.errors import RateLimitExceeded
from werkzeug.exceptions import HTTPException

from services.api_response import error_response
from services.exceptions import ApiError


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(error: RateLimitExceeded):
        current_app.logger.warning(
            "rate_limit_violation method=%s path=%s remote_addr=%s limit=%s",
            request.method,
            request.path,
            request.headers.get("X-Forwarded-For", request.remote_addr),
            error.description,
        )
        return error_response(
            message="Rate limit exceeded",
            status_code=429,
            code="rate_limit_exceeded",
            details=None,
        )

    @app.errorhandler(ApiError)
    def handle_api_error(error: ApiError):
        return error_response(
            message=error.message,
            status_code=error.status_code,
            code=error.code,
            details=error.details,
        )

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        return error_response(
            message=error.description,
            status_code=error.code or 500,
            code=error.name.lower().replace(" ", "_"),
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        current_app.logger.exception(
            "Unhandled exception for %s %s",
            request.method,
            request.path,
        )
        return error_response(
            message="An unexpected server error occurred.",
            status_code=500,
            code="internal_error",
        )
