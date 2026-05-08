# ai-service/routes/generate_report.py

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from flask import Blueprint, request, jsonify
from middleware.helpers import validate_input, sanitise_all_fields, parse_json_body
from services.groq_client import GroqClient
from services.cache_service import cache
from services.fallback_service import get_generate_report_fallback

logger             = logging.getLogger(__name__)
generate_report_bp = Blueprint("generate_report", __name__)
client             = GroqClient()

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "generate_report.txt"


def load_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


@generate_report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    """
    Generate a full professional incident report.

    Request Body:
    {
        "title":           "Ransomware Attack",
        "incident_type":   "Ransomware",
        "severity":        "Critical",
        "affected_system": "File Server",
        "description":     "2TB of data encrypted..."
    }

    Response:
    {
        "success":      true,
        "is_fallback":  false,
        "generated_at": "2024-04-21T10:30:00Z",
        "report":       { ...full report object... },
        "usage":        { "model": "...", "total_tokens_used": 800 }
    }
    """
    logger.info("POST /generate-report called")

    # Step 1 — Parse JSON
    parsed = parse_json_body(request)
    if not parsed["valid"]:
        logger.warning(f"POST /generate-report — JSON parse failed: {parsed['reason']}")
        return jsonify({"error": "Bad request", "message": parsed["reason"], "status": 400}), 400

    data = parsed["data"]

    # Step 2 — Validate
    validation = validate_input(data)
    if not validation["valid"]:
        logger.warning(f"POST /generate-report — validation failed: {validation['reason']}")
        return jsonify({"error": "Validation failed", "message": validation["reason"], "status": 400}), 400

    # Step 3 — Sanitise
    sanitised = sanitise_all_fields(data)
    if not sanitised["safe"]:
        logger.warning(f"POST /generate-report — sanitisation failed: {sanitised['reason']}")
        return jsonify({"error": "Invalid input", "message": sanitised["reason"], "status": 400}), 400

    clean = sanitised["sanitised"]

    # Step 4 — Check cache
    cached = cache.get("generate_report", clean)
    if cached:
        return jsonify(cached), 200

    # Step 5 — Build prompt
    now = datetime.now(timezone.utc).isoformat()
    try:
        prompt = load_prompt().format(
            **clean,
            reported_at  = now,
            generated_at = now
        )
    except Exception as e:
        logger.error(f"POST /generate-report — prompt load failed: {str(e)}")
        return jsonify({"error": "Internal server error", "message": "Failed to load prompt template", "status": 500}), 500

    # Step 6 — Call Groq
    try:
        groq_response = client.call(prompt=prompt)
    except RuntimeError:
        return jsonify(get_generate_report_fallback(clean)), 200

    # Step 7 — Parse response
    try:
        ai_data = json.loads(groq_response["content"])
        if isinstance(ai_data, dict) and "error" in ai_data:
            return jsonify({"error": "Invalid input", "message": ai_data["error"], "status": 400}), 400
    except json.JSONDecodeError as e:
        logger.error(f"POST /generate-report — JSON parse failed: {str(e)}")
        return jsonify({"error": "AI response error", "message": "AI returned invalid JSON — please retry", "status": 502}), 502

    # Step 8 — Build and cache response
    response = {
        "success":      True,
        "is_fallback":  False,
        "generated_at": now,
        "report":       ai_data,
        "usage": {
            "model":             groq_response["model"],
            "total_tokens_used": groq_response["usage"]["total_tokens"]
        }
    }
    cache.set("generate_report", clean, response)
    return jsonify(response), 200