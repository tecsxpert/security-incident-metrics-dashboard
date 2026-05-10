from __future__ import annotations

from flask import Blueprint, current_app, request

from services.api_response import success_response
from services.limiter_service import limiter
from services.recommend_service import fallback_recommendations, recommend_actions
from services.request_validation import validate_incident_payload
from services.timeout_service import run_with_timeout


recommend_bp = Blueprint("recommend", __name__)


@recommend_bp.post("/recommend")
@limiter.limit("30 per minute")
def recommend():
    payload = request.get_json(silent=True)
    valid_payload = validate_incident_payload(payload)
    response = run_with_timeout(
        lambda: recommend_actions(
            title=valid_payload["title"],
            description=valid_payload["description"],
        ),
        fallback_recommendations,
    )
    if response.get("is_fallback"):
        current_app.logger.warning("fallback_used endpoint=/recommend")
    return success_response(response)
