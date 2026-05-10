from __future__ import annotations

import html
import re
from html.parser import HTMLParser

from services.exceptions import ValidationError


PROMPT_INJECTION_PATTERNS = [
    r"\bignore\s+(all\s+)?(previous|prior|above)\s+(instructions|rules|prompt)\b",
    r"\bdisregard\s+(all\s+)?(previous|prior|above)\s+(instructions|rules|prompt)\b",
    r"\boverride\s+(the\s+)?(system|developer|previous)\s+(prompt|instructions|message)\b",
    r"\breveal\s+(the\s+)?(system\s+prompt|hidden\s+prompt|developer\s+message|instructions)\b",
    r"\bshow\s+(me\s+)?(the\s+)?(system\s+prompt|hidden\s+prompt|developer\s+message)\b",
    r"\byou\s+are\s+now\s+(in\s+)?(developer|system|admin|root)\s+mode\b",
    r"\bact\s+as\s+(a\s+)?(system|developer|admin|root)\b",
    r"\breturn\s+(only\s+)?(plain\s+text|markdown|xml|html)\b",
    r"\bdo\s+not\s+return\s+json\b",
    r"\bforget\s+(your\s+)?(instructions|rules|prompt)\b",
]


class _HTMLStripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self._parts.append(data)

    def get_data(self) -> str:
        return "".join(self._parts)


def strip_html(value: str) -> str:
    stripper = _HTMLStripper()
    stripper.feed(value)
    stripper.close()
    return html.unescape(stripper.get_data())


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def sanitize_text(value: str) -> str:
    return normalize_whitespace(strip_html(value))


def detect_prompt_injection(value: str) -> bool:
    normalized = normalize_whitespace(value).lower()
    return any(re.search(pattern, normalized, flags=re.IGNORECASE) for pattern in PROMPT_INJECTION_PATTERNS)


def sanitize_and_validate_text(field_name: str, value: object, max_length: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"Field '{field_name}' is required and must be a non-empty string.")

    if detect_prompt_injection(value):
        raise ValidationError(
            f"Field '{field_name}' contains unsafe prompt-injection content.",
            details={"field": field_name},
        )

    sanitized = sanitize_text(value)
    if not sanitized:
        raise ValidationError(f"Field '{field_name}' is empty after sanitization.")

    if len(sanitized) > max_length:
        raise ValidationError(f"Field '{field_name}' must be {max_length} characters or fewer.")

    return sanitized
