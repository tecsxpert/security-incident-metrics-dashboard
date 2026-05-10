from __future__ import annotations

from services.exceptions import ValidationError
from services.security_service import sanitize_and_validate_text


def validate_incident_payload(payload: object) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be a JSON object.")

    title = sanitize_and_validate_text("title", payload.get("title"), max_length=250)
    description = sanitize_and_validate_text("description", payload.get("description"), max_length=5000)

    return {"title": title, "description": description}


def validate_report_payload(payload: object) -> dict[str, list[dict[str, str]]]:
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be a JSON object.")

    if "incidents" not in payload:
        legacy = validate_incident_payload(payload)
        return {
            "incidents": [
                {
                    "title": legacy["title"],
                    "severity": "unknown",
                    "summary": legacy["description"],
                }
            ]
        }

    incidents = payload.get("incidents")
    if not isinstance(incidents, list) or not incidents:
        raise ValidationError("Field 'incidents' is required and must be a non-empty array.")

    if len(incidents) > 50:
        raise ValidationError("Field 'incidents' must contain 50 items or fewer.")

    validated: list[dict[str, str]] = []
    for index, incident in enumerate(incidents):
        if not isinstance(incident, dict):
            raise ValidationError(f"Incident at index {index} must be a JSON object.")

        title = sanitize_and_validate_text(f"incidents[{index}].title", incident.get("title"), max_length=250)
        severity = sanitize_and_validate_text(f"incidents[{index}].severity", incident.get("severity"), max_length=30)
        summary = sanitize_and_validate_text(f"incidents[{index}].summary", incident.get("summary"), max_length=1000)

        severity = severity.lower()
        if severity not in {"critical", "high", "medium", "low", "unknown"}:
            raise ValidationError(
                f"Incident at index {index} has unsupported severity.",
                details={"field": f"incidents[{index}].severity"},
            )

        validated.append(
            {
                "title": title,
                "severity": severity,
                "summary": summary,
            }
        )

    return {"incidents": validated}
