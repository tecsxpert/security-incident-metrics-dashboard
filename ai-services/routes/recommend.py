# ai-service/routes/recommend.py

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from flask import Blueprint, request, jsonify
from middleware.helpers import validate_input, sanitise_all_fields, parse_json_body
from services.groq_client import GroqClient
from services.cache_service import cache
from services.fallback_service import get_recommend_fallback

logger       = logging.getLogger(__name__)
recommend_bp = Blueprint("recommend", __name__)
client       = GroqClient()

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "recommend.txt"


def load_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def validate_recommendations(recommendations: list) -> bool:
    if not isinstance(recommendations, list) or len(recommendations) != 3:
        return False
    required_keys = {"action_type", "description", "priority"}
    for rec in recommendations:
        if not isinstance(rec, dict):
            return False
        if not required_keys.issubset(rec.keys()):
            return False
        if not all(str(rec[k]).strip() for k in required_keys):
            return False
    return True


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    """
    Generate 3 actionable recommendations for a security incident.

    Request Body:
    {
        "title":           "Phishing Attack",
        "incident_type":   "Phishing",
        "severity":        "High",
        "affected_system": "Email Server",
        "description":     "15 employees received phishing emails..."
    }

    Response:
    {
        "success":         true,
        "is_fallback":     false,
        "generated_at":    "2024-04-21T10:30:00Z",
        "recommendations": [ { "action_type": "...", "description": "...", "priority": "..." } ],
        "usage":           { "model": "...", "total_tokens_used": 320 }
    }
    """
    logger.info("POST /recommend called")

    # Step 1 — Parse JSON
    parsed = parse_json_body(request)
    if not parsed["valid"]:
        logger.warning(f"POST /recommend — JSON parse failed: {parsed['reason']}")
        return jsonify({"error": "Bad request", "message": parsed["reason"], "status": 400}), 400

    data = parsed["data"]

    # Step 2 — Validate
    validation = validate_input(data)
    if not validation["valid"]:
        logger.warning(f"POST /recommend — validation failed: {validation['reason']}")
        return jsonify({"error": "Validation failed", "message": validation["reason"], "status": 400}), 400

    # Step 3 — Sanitise
    sanitised = sanitise_all_fields(data)
    if not sanitised["safe"]:
        logger.warning(f"POST /recommend — sanitisation failed: {sanitised['reason']}")
        return jsonify({"error": "Invalid input", "message": sanitised["reason"], "status": 400}), 400

    clean = sanitised["sanitised"]

    # Step 4 — Check cache
    cached = cache.get("recommend", clean)
    if cached:
        return jsonify(cached), 200

    # Step 5 — Build prompt
    try:
        prompt = load_prompt().format(**clean)
    except Exception as e:
        logger.error(f"POST /recommend — prompt load failed: {str(e)}")
        return jsonify({"error": "Internal server error", "message": "Failed to load prompt template", "status": 500}), 500

    # Step 6 — Call Groq
    try:
        groq_response = client.call(prompt=prompt)
    except RuntimeError:
        return jsonify(get_recommend_fallback(clean)), 200

    # Step 7 — Parse response
    try:
        ai_data = json.loads(groq_response["content"])
        if isinstance(ai_data, dict) and "error" in ai_data:
            return jsonify({"error": "Invalid input", "message": ai_data["error"], "status": 400}), 400
        if isinstance(ai_data, list):
            recommendations = ai_data
        else:
            recommendations = ai_data.get("recommendations", ai_data)
    except json.JSONDecodeError as e:
        logger.error(f"POST /recommend — JSON parse failed: {str(e)}")
        return jsonify({"error": "AI response error", "message": "AI returned invalid JSON — please retry", "status": 502}), 502

    # Step 8 — Validate structure
    if not validate_recommendations(recommendations):
        logger.error("POST /recommend — invalid recommendations structure")
        return jsonify({"error": "AI response error", "message": "AI returned unexpected format — please retry", "status": 502}), 502

    # Step 9 — Build and cache response
    response = {
        "success":         True,
        "is_fallback":     False,
        "generated_at":    datetime.now(timezone.utc).isoformat(),
        "recommendations": recommendations,
        "usage": {
            "model":             groq_response["model"],
            "total_tokens_used": groq_response["usage"]["total_tokens"]
        }
    }
    cache.set("recommend", clean, response)
    return jsonify(response), 200