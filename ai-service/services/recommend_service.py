from __future__ import annotations

import json
import logging
from typing import Any

from services.cache_service import build_cache_key, redis_cache
from services.groq_service import GroqService
from services.prompt_service import load_prompt_template


logger = logging.getLogger(__name__)

ALLOWED_PRIORITIES = {"critical", "high", "medium", "low"}
ALLOWED_ACTION_TYPES = {"triage", "containment", "remediation", "monitoring", "validation"}
MAX_RECOMMENDATION_WORDS = 20


def fallback_recommendation_items() -> list[dict[str, str]]:
    return [
        {
            "action_type": "triage",
            "description": "Review the incident details and confirm the affected asset, observed indicators, and current impact.",
            "priority": "medium",
        },
        {
            "action_type": "containment",
            "description": "Preserve relevant logs and isolate affected systems if there is evidence of active compromise.",
            "priority": "medium",
        },
        {
            "action_type": "validation",
            "description": "Assign an analyst to validate the alert and document confirmed findings before remediation.",
            "priority": "low",
        },
    ]


def _trim_words(text: str, max_words: int = MAX_RECOMMENDATION_WORDS) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(" ,.;:") + "."


def fallback_recommendations() -> dict[str, Any]:
    return {
        "recommendations": fallback_recommendation_items(),
        "is_fallback": True,
    }


def build_recommend_prompt(title: str, description: str) -> str:
    template = load_prompt_template("recommend_prompt.txt")
    incident_data = {
        "title": title,
        "description": description,
    }
    return template.replace("{{incident_data}}", json.dumps(incident_data, ensure_ascii=False))


def _normalize_item(item: Any, fallback: dict[str, str]) -> dict[str, str]:
    if not isinstance(item, dict):
        return fallback

    action_type = item.get("action_type") or item.get("title") or fallback["action_type"]
    description = item.get("description") or item.get("action") or fallback["description"]
    priority = str(item.get("priority", fallback["priority"])).lower()

    if not isinstance(action_type, str) or not action_type.strip():
        action_type = fallback["action_type"]

    if not isinstance(description, str) or not description.strip():
        description = fallback["description"]

    if priority not in ALLOWED_PRIORITIES:
        priority = fallback["priority"]

    normalized_action = action_type.strip().lower().replace(" ", "_")
    if normalized_action not in ALLOWED_ACTION_TYPES:
        normalized_action = fallback["action_type"]

    return {
        "action_type": normalized_action,
        "description": _trim_words(description.strip()),
        "priority": priority,
    }


def normalize_recommendations(data: Any) -> list[dict[str, str]]:
    fallback = fallback_recommendation_items()
    raw_items = data if isinstance(data, list) else data.get("recommendations") if isinstance(data, dict) else None

    if not isinstance(raw_items, list):
        logger.warning("recommend_parse_failure reason=missing_recommendations_array")
        raw_items = []

    normalized = [
        _normalize_item(raw_items[index], fallback[index])
        if index < len(raw_items)
        else fallback[index]
        for index in range(3)
    ]
    return normalized


def recommend_actions(title: str, description: str) -> dict[str, Any]:
    try:
        cache_payload = {"title": title, "description": description}
        cache_key = build_cache_key("recommend", cache_payload)
        cached = redis_cache.get(cache_key)
        if isinstance(cached, dict):
            return cached

        prompt = build_recommend_prompt(title, description)
        groq_response = GroqService().generate_json(prompt)
        recommendations = normalize_recommendations(groq_response)
        response = {
            "recommendations": recommendations,
            "is_fallback": False,
        }
        redis_cache.set(cache_key, response)
        return response
    except Exception as exc:
        logger.exception(
            "fallback_triggered endpoint=/recommend exception_type=%s",
            type(exc).__name__,
        )
        return fallback_recommendations()
