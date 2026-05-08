# ai-service/middleware/sanitiser.py

import re
import bleach
import logging

logger = logging.getLogger(__name__)

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|above|prior)\s+instructions?",
    r"forget\s+(all\s+)?(previous|above|prior)\s+instructions?",
    r"you\s+are\s+now\s+a",
    r"act\s+as\s+(a\s+)?(?!cybersecurity)",
    r"pretend\s+(you\s+are|to\s+be)",
    r"your\s+new\s+role\s+is",
    r"disregard\s+(all\s+)?(previous|prior)\s+instructions?",
    r"override\s+(your\s+)?(instructions?|rules?|guidelines?)",
    r"reveal\s+(your\s+)?(system\s+)?(prompt|instructions?|api\s+key)",
    r"print\s+(your\s+)?(system\s+)?(prompt|instructions?)",
    r"what\s+are\s+your\s+instructions",
    r"jailbreak",
    r"dan\s+mode",
    r"developer\s+mode",
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]


def strip_html(text: str) -> str:
    return bleach.clean(text, tags=[], strip=True).strip()


def detect_prompt_injection(text: str) -> bool:
    for pattern in COMPILED_PATTERNS:
        if pattern.search(text):
            logger.warning(f"Prompt injection detected — pattern: '{pattern.pattern}' in input: '{text[:80]}'")
            return True
    return False


def sanitise_input(text: str) -> dict:
    if not text or not text.strip():
        return {"safe": False, "cleaned": "", "reason": "Input is empty or blank"}

    cleaned = strip_html(text)

    if len(cleaned) > 2000:
        logger.warning(f"Input too long — {len(cleaned)} chars")
        return {"safe": False, "cleaned": cleaned, "reason": "Input exceeds maximum allowed length of 2000 characters"}

    if detect_prompt_injection(cleaned):
        return {"safe": False, "cleaned": cleaned, "reason": "Potential prompt injection detected in input"}

    return {"safe": True, "cleaned": cleaned, "reason": None}