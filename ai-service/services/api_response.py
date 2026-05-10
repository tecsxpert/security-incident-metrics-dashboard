from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from flask import jsonify
from werkzeug.wrappers import Response


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def success_response(data: Any, status_code: int = 200) -> tuple[Response, int]:
    return jsonify(
        {
            "success": True,
            "data": data,
            "error": None,
            "meta": {
                "generated_at": utc_now_iso(),
            },
        }
    ), status_code


def error_response(
    message: str,
    status_code: int,
    code: str = "request_error",
    details: Any | None = None,
) -> tuple[Response, int]:
    return jsonify(
        {
            "success": False,
            "data": None,
            "error": {
                "code": code,
                "message": message,
                "details": details,
            },
            "meta": {
                "generated_at": utc_now_iso(),
            },
        }
    ), status_code
