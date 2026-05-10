from __future__ import annotations

from flask import Blueprint, current_app, request

from services.api_response import success_response, error_response
from services.describe_service import describe_incident, fallback_describe_response
from services.exceptions import ValidationError
from services.limiter_service import limiter
from services.request_validation import validate_incident_payload
from services.timeout_service import run_with_timeout


describe_bp = Blueprint("describe", __name__)


@describe_bp.post("/describe")
@limiter.limit("30 per minute")
def describe():
    try:
        print(" /describe endpoint hit")

        # 🔹 Get JSON payload
        payload = request.get_json(silent=True)

        if payload is None:
            return error_response(
                message="Request body must be valid JSON",
                status_code=400,
                code="invalid_json",
            )

        # 🔹 Validate input
        valid_payload = validate_incident_payload(payload)
        title = valid_payload["title"]
        description = valid_payload["description"]

        print(" Input:", title, "|", description)

        # 🔹 Call AI with timeout
        ai_result = run_with_timeout(
            lambda: describe_incident(
                title=title,
                description=description,
            ),
            fallback_describe_response,
        )

        print(" AI RESULT:", ai_result)
        if ai_result.get("is_fallback"):
            current_app.logger.warning("fallback_used endpoint=/describe")

        # 🔹 Ensure safe output
        summary = ai_result.get("summary", "No summary available")
        severity = str(ai_result.get("severity", "unknown")).lower()

        # Normalize severity
        if severity not in {"critical", "high", "medium", "low", "unknown"}:
            severity = "unknown"

        response_data = {
            "summary": summary,
            "severity": severity,
            "is_fallback": ai_result.get("is_fallback", False)
        }

        return success_response(response_data)

    except ValidationError as ve:
        return error_response(
            message=ve.message,
            status_code=ve.status_code,
            code=ve.code,
            details=ve.details,
        )

    except Exception as e:
        print("ERROR:", str(e))
        return error_response(
            message="Something went wrong while processing the request",
            status_code=500,
            code="internal_error",
        )
