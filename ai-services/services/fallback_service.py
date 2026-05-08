# ai-service/services/fallback_service.py

import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def get_describe_fallback(data: dict) -> dict:
    logger.warning("Using fallback template for /describe")
    return {
        "success":      True,
        "is_fallback":  True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data": {
            "summary":                f"A {data.get('severity')} severity '{data.get('incident_type')}' incident affecting {data.get('affected_system')}. AI analysis temporarily unavailable.",
            "attack_vector":          "Manual analysis required — AI service unavailable.",
            "impact":                 "Manual analysis required — AI service unavailable.",
            "indicators":             ["Manual investigation required"],
            "severity_justification": f"Severity reported as {data.get('severity')} — requires manual verification."
        },
        "usage": {"model": "fallback", "total_tokens_used": 0}
    }


def get_recommend_fallback(data: dict) -> dict:
    logger.warning("Using fallback template for /recommend")
    return {
        "success":         True,
        "is_fallback":     True,
        "generated_at":    datetime.now(timezone.utc).isoformat(),
        "recommendations": [
            {"action_type": "containment", "description": "Isolate affected systems immediately.", "priority": "Immediate"},
            {"action_type": "eradication", "description": "Engage incident response team to investigate.", "priority": "High"},
            {"action_type": "prevention",  "description": "Review and update security policies post-incident.", "priority": "Medium"},
        ],
        "usage": {"model": "fallback", "total_tokens_used": 0}
    }


def get_generate_report_fallback(data: dict) -> dict:
    logger.warning("Using fallback template for /generate-report")
    now = datetime.now(timezone.utc).isoformat()
    return {
        "success":      True,
        "is_fallback":  True,
        "generated_at": now,
        "report": {
            "report_title":      f"Incident Report — {data.get('title', 'Unknown')}",
            "executive_summary": f"A {data.get('severity')} severity incident was reported. AI report generation temporarily unavailable.",
            "incident_timeline": [
                {"time": "T+0h", "event": "Incident reported"},
                {"time": "T+1h", "event": "Investigation initiated"},
            ],
            "technical_analysis": {
                "attack_vector":            "Manual analysis required",
                "affected_components":      [data.get("affected_system", "Unknown")],
                "data_at_risk":             "Manual analysis required",
                "indicators_of_compromise": ["Manual investigation required"]
            },
            "impact_assessment": {
                "business_impact": "Manual analysis required",
                "data_impact":     "Manual analysis required",
                "user_impact":     "Manual analysis required"
            },
            "remediation": {
                "immediate_actions":         ["Isolate affected systems", "Notify security team"],
                "long_term_recommendations": ["Review security policies", "Update incident response plan"]
            },
            "lessons_learned":     ["Manual review required"],
            "risk_rating":         data.get("severity", "Unknown"),
            "report_generated_at": now
        },
        "usage": {"model": "fallback", "total_tokens_used": 0}
    }