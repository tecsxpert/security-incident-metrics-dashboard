from __future__ import annotations

from typing import Any


class ApiError(Exception):
    status_code = 500
    code = "internal_error"

    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class ValidationError(ApiError):
    status_code = 400
    code = "validation_error"
