from __future__ import annotations

import json
import logging
from typing import Any

from services.cache_service import build_cache_key, redis_cache
from services.groq_service import GroqService
from services.prompt_service import load_prompt_template


logger = logging.getLogger(__name__)


def fallback_report() -> dict[str, Any]:
    return {
        "title": "Incident Report Unavailable",
        "summary": "SOC report generation is temporarily unavailable.",
        "overview": "The service could not complete AI synthesis. Review incident evidence manually for shared indicators, affected identities, and compromise risk.",
        "key_items": [],
        "recommendations": [],
        "is_fallback": True,
    }


def build_report_prompt(incidents: list[dict[str, str]]) -> str:
    template = load_prompt_template("report_prompt.txt")
    incident_data = {
        "incidents": incidents,
    }
    return template.replace("{{incident_data}}", json.dumps(incident_data, ensure_ascii=False))


def _string_or_default(value: Any, default: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return default


def _normalize_string_list(value: Any, fallback: list[str] | None = None) -> list[str]:
    if not isinstance(value, list):
        return fallback or []

    normalized: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            normalized.append(item.strip())
        elif isinstance(item, dict):
            text = item.get("item") or item.get("description") or item.get("action") or item.get("title")
            if isinstance(text, str) and text.strip():
                normalized.append(text.strip())

    return normalized


def _normalize_overview(value: Any) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()

    if isinstance(value, dict):
        parts: list[str] = []
        incident_type = value.get("incident_type")
        business_impact = value.get("business_impact")
        affected_assets = value.get("affected_assets")

        if isinstance(incident_type, str) and incident_type.strip():
            parts.append(f"Incident type: {incident_type.strip()}.")
        if isinstance(affected_assets, list) and affected_assets:
            assets = ", ".join(str(asset) for asset in affected_assets if str(asset).strip())
            if assets:
                parts.append(f"Affected assets: {assets}.")
        if isinstance(business_impact, str) and business_impact.strip():
            parts.append(f"Business impact: {business_impact.strip()}.")

        if parts:
            return " ".join(parts)

    return "No detailed overview was generated."


def _fallback_title(incidents: list[dict[str, str]]) -> str:
    if len(incidents) == 1:
        return f"SOC Incident Report: {incidents[0]['title']}"
    return "SOC Incident Intelligence Report"


def _fallback_key_items(incidents: list[dict[str, str]]) -> list[str]:
    items: list[str] = []
    combined = " ".join(f"{incident['title']} {incident['summary']}" for incident in incidents).lower()

    if any(term in combined for term in ["failed login", "successful login", "vpn", "authentication"]):
        items.append("Authentication activity indicates possible credential abuse against remote access infrastructure.")
    if any(term in combined for term in ["unknown ip", "unknown source", "unusual location", "suspicious location"]):
        items.append("Source anomalies require validation against expected user locations and trusted networks.")
    if any(term in combined for term in ["malware", "edr", "ransomware"]):
        items.append("Endpoint indicators suggest malware containment and blast-radius validation may be required.")
    if any(term in combined for term in ["phishing", "email", "credential harvest"]):
        items.append("Phishing indicators may be contributing to credential exposure risk.")

    if not items:
        items.append("Incident set requires analyst review to confirm common indicators and operational impact.")

    return items[:5]


def fallback_report_for_incidents(incidents: list[dict[str, str]]) -> dict[str, Any]:
    high_risk = [incident for incident in incidents if incident["severity"] in {"critical", "high"}]
    summary = (
        f"{len(incidents)} incidents reviewed; {len(high_risk)} high-risk items indicate elevated compromise risk."
        if len(incidents) > 1
        else incidents[0]["summary"]
    )
    key_items = _fallback_key_items(incidents)

    return {
        "title": _fallback_title(incidents),
        "summary": summary,
        "overview": "The incident set requires correlation across identities, endpoints, source infrastructure, and timestamps to confirm recurring attack patterns before closure.",
        "key_items": key_items,
        "recommendations": [
            "Correlate incidents by source IP, account, asset, and timestamp to identify repeated activity.",
            "Prioritize investigation of critical and high severity incidents for active compromise evidence.",
            "Document confirmed indicators and apply containment controls only where supported by logs.",
        ],
        "is_fallback": True,
    }


def normalize_report(data: dict[str, Any], incidents: list[dict[str, str]]) -> dict[str, Any]:
    title = _string_or_default(data.get("title"), _fallback_title(incidents))
    summary = _string_or_default(data.get("summary"), fallback_report_for_incidents(incidents)["summary"])
    overview = _normalize_overview(data.get("overview"))
    key_items = _normalize_string_list(data.get("key_items"), fallback=_fallback_key_items(incidents))
    recommendations = _normalize_string_list(data.get("recommendations"))

    if not recommendations:
        recommendations = fallback_report_for_incidents(incidents)["recommendations"]

    return {
        "title": title,
        "summary": summary,
        "overview": overview,
        "key_items": key_items[:8],
        "recommendations": recommendations[:8],
    }


def generate_report(incidents: list[dict[str, str]]) -> dict[str, Any]:
    try:
        cache_payload = {"incidents": incidents}
        cache_key = build_cache_key("generate-report", cache_payload)
        cached = redis_cache.get(cache_key)
        if isinstance(cached, dict):
            return cached

        prompt = build_report_prompt(incidents)
        groq_response = GroqService().generate_json(prompt)
        if not isinstance(groq_response, dict):
            logger.warning("report_parse_failure reason=non_object_response")
            return fallback_report_for_incidents(incidents)

        report = normalize_report(groq_response, incidents)
        report["is_fallback"] = False
        redis_cache.set(cache_key, report)
        return report
    except Exception as exc:
        logger.exception(
            "fallback_triggered endpoint=/generate-report exception_type=%s",
            type(exc).__name__,
        )
        return fallback_report_for_incidents(incidents)
