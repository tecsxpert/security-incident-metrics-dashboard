# ai-service/routes/describe.py

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from flask import Blueprint, request, jsonify
from middleware.helpers import validate_input, sanitise_all_fields, parse_json_body
from services.groq_client import GroqClient
from services.cache_service import cache
from services.fallback_service import get_describe_fallback

logger      = logging.getLogger(__name__)
describe_bp = Blueprint("describe", __name__)
client      = GroqClient()

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "describe.txt"


def load_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


@describe_bp.route("/describe", methods=["POST"])
def describe():
    logger.info("POST /describe called")

    parsed = parse_json_body(request)
    if not parsed["valid"]:
        logger.warning(f"POST /describe — JSON parse failed: {parsed['reason']}")
        return jsonify({"error": "Bad request", "message": parsed["reason"], "status": 400}), 400

    data = parsed["data"]

    validation = validate_input(data)
    if not validation["valid"]:
        logger.warning(f"POST /describe — validation failed: {validation['reason']}")
        return jsonify({"error": "Validation failed", "message": validation["reason"], "status": 400}), 400

    sanitised = sanitise_all_fields(data)
    if not sanitised["safe"]:
        logger.warning(f"POST /describe — sanitisation failed: {sanitised['reason']}")
        return jsonify({"error": "Invalid input", "message": sanitised["reason"], "status": 400}), 400

    clean = sanitised["sanitised"]

    cached = cache.get("describe", clean)
    if cached:
        return jsonify(cached), 200

    try:
        prompt = load_prompt().format(**clean)
    except Exception as e:
        logger.error(f"POST /describe — prompt load failed: {str(e)}")
        return jsonify({"error": "Internal server error", "message": "Failed to load prompt template", "status": 500}), 500

    try:
        groq_response = client.call(prompt=prompt)
    except RuntimeError:
        return jsonify(get_describe_fallback(clean)), 200

    try:
        ai_data = json.loads(groq_response["content"])
        if isinstance(ai_data, dict) and "error" in ai_data:
            return jsonify({"error": "Invalid input", "message": ai_data["error"], "status": 400}), 400
    except json.JSONDecodeError as e:
        logger.error(f"POST /describe — JSON parse failed: {str(e)}")
        return jsonify({"error": "AI response error", "message": "AI returned invalid JSON — please retry", "status": 502}), 502

    response = {
        "success":      True,
        "is_fallback":  False,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data":         ai_data,
        "usage": {"model": groq_response["model"], "total_tokens_used": groq_response["usage"]["total_tokens"]}
    }
    cache.set("describe", clean, response)
    return jsonify(response), 200