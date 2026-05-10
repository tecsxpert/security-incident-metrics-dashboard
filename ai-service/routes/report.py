from __future__ import annotations

import inspect

from flask import Blueprint, current_app, request

from services.api_response import success_response
from services.limiter_service import limiter
from services.report_service import fallback_report_for_incidents, generate_report
from services.request_validation import validate_report_payload
from services.timeout_service import run_with_timeout


report_bp = Blueprint("report", __name__)


def _generate_report_compatible(incidents: list[dict[str, str]]):
    if len(inspect.signature(generate_report).parameters) == 1:
        return generate_report(incidents)

    first = incidents[0]
    return generate_report(first["title"], first["summary"])


@report_bp.post("/generate-report")
@limiter.limit("30 per minute")
def generate_report_route():
    payload = request.get_json(silent=True)
    valid_payload = validate_report_payload(payload)
    incidents = valid_payload["incidents"]
    response = run_with_timeout(
        lambda: _generate_report_compatible(incidents),
        lambda: fallback_report_for_incidents(incidents),
    )
    if response.get("is_fallback"):
        current_app.logger.warning("fallback_used endpoint=/generate-report")
    return success_response(response)
