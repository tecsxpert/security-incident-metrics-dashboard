from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from services.cache_service import build_cache_key, redis_cache
from services.groq_service import GroqService
from services.prompt_service import load_prompt_template


logger = logging.getLogger(__name__)

ALLOWED_SEVERITIES = {"critical", "high", "medium", "low"}
MAX_SUMMARY_WORDS = 30


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# Fallback response (safe)
def fallback_describe_response() -> dict[str, str | bool]:
    return {
        "summary": "Unable to generate incident summary at this time.",
        "severity": "unknown",
        "generated_at": utc_now_iso(),
        "is_fallback": True,
    }


#  Build prompt with strict contract
def build_describe_prompt(title: str, description: str) -> str:
    template = load_prompt_template("describe_prompt.txt")

    incident_data = {
        "title": title,
        "description": description,
    }

    return template.replace("{{incident_data}}", json.dumps(incident_data, ensure_ascii=False))


def trim_summary_words(summary: str, max_words: int = MAX_SUMMARY_WORDS) -> str:
    words = summary.split()
    if len(words) <= max_words:
        return summary
    return " ".join(words[:max_words]).rstrip(" ,.;:") + "."


#  Normalize output
def normalize_describe_response(data: dict[str, Any]) -> dict[str, str]:
    summary = data.get("summary") or data.get("description") or data.get("title")
    severity = str(data.get("severity", "unknown")).lower()

    if not isinstance(summary, str) or not summary.strip():
        summary = "No incident summary was generated."

    if severity not in ALLOWED_SEVERITIES:
        severity = infer_severity(summary)

    return {
        "summary": trim_summary_words(summary.strip()),
        "severity": severity,
        "generated_at": utc_now_iso(),
    }


def infer_severity(text: str) -> str:
    normalized = text.lower()
    if any(term in normalized for term in ["privilege escalation", "ransomware", "data exfiltration", "domain admin"]):
        return "critical"
    if any(term in normalized for term in ["successful login", "unknown ip", "malware", "compromise", "lateral movement"]):
        return "high"
    if any(term in normalized for term in ["failed login", "phishing", "suspicious", "alert"]):
        return "medium"
    return "low"


# MAIN FUNCTION (fixed properly)
def describe_incident(title: str, description: str) -> dict[str, str | bool]:
    try:
        #  Cache check
        cache_payload = {"title": title, "description": description}
        cache_key = build_cache_key("describe", cache_payload)

        cached = redis_cache.get(cache_key)
        if isinstance(cached, dict):
            return cached

        #  Build prompt
        prompt = build_describe_prompt(title, description)

        
        groq_response = GroqService().generate_json(prompt)
        if not isinstance(groq_response, dict):
            logger.warning("describe_parse_failure reason=non_object_response")
            return fallback_describe_response()

        #  Normalize
        normalized = normalize_describe_response(groq_response)
        normalized["is_fallback"] = False

        #  Cache result
        redis_cache.set(cache_key, normalized)

        return normalized

    except Exception as exc:
        logger.exception(
            "fallback_triggered endpoint=/describe exception_type=%s",
            type(exc).__name__,
        )
        return fallback_describe_response()
