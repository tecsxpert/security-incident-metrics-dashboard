from __future__ import annotations

from flask import Flask, request

from services.exceptions import ValidationError


JSON_ENDPOINTS = {"/describe", "/recommend", "/generate-report"}


def register_security_middleware(app: Flask) -> None:
    @app.before_request
    def enforce_json_requests() -> None:
        if request.path in JSON_ENDPOINTS and request.method == "POST" and not request.is_json:
            raise ValidationError("Content-Type must be application/json.")

    @app.after_request
    def add_security_headers(response):
        # Prevent MIME sniffing so browsers honor the JSON content type.
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Block clickjacking by preventing the API response from being framed.
        response.headers["X-Frame-Options"] = "DENY"
        # Avoid leaking request paths or query details to downstream sites.
        response.headers["Referrer-Policy"] = "no-referrer"
        # Keep incident data out of browser and intermediary caches.
        response.headers["Cache-Control"] = "no-store"
        # Deny all browser-loaded content and explicitly forbid framing.
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        return response
