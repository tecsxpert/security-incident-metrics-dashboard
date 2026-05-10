from __future__ import annotations

import json
import logging
import os
import re
import time
from typing import Any

logger = logging.getLogger(__name__)


class GroqServiceError(RuntimeError):
    pass


def _recover_json_text(content: str) -> str:
    cleaned = content.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    if cleaned.startswith("{") or cleaned.startswith("["):
        return cleaned

    object_match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    array_match = re.search(r"\[.*\]", cleaned, flags=re.DOTALL)

    if object_match and array_match:
        return object_match.group() if object_match.start() < array_match.start() else array_match.group()
    if object_match:
        return object_match.group()
    if array_match:
        return array_match.group()

    return cleaned


def _extract_json(content: str) -> Any:
    recovered = _recover_json_text(content)

    try:
        parsed = json.loads(recovered)
    except json.JSONDecodeError as exc:
        logger.error(
            "parse_failure service=groq exception_type=%s raw_response=%s",
            type(exc).__name__,
            content,
        )
        raise GroqServiceError("Groq response was not valid JSON") from exc

    if not isinstance(parsed, (dict, list)):
        raise GroqServiceError("Groq response JSON must be an object or array")

    return parsed


class GroqService:
    def __init__(self) -> None:
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

       
        self.timeout_seconds = float(os.getenv("GROQ_TIMEOUT_SECONDS", "5"))

        self.retry_attempts = int(os.getenv("GROQ_RETRY_ATTEMPTS", "3"))
        self.retry_backoff_seconds = float(os.getenv("GROQ_RETRY_BACKOFF_SECONDS", "0.5"))

        if not self.api_key:
            raise GroqServiceError("GROQ_API_KEY is not configured")

        from groq import Groq

        self.client = Groq(
            api_key=self.api_key,
            timeout=self.timeout_seconds,
            max_retries=0,
        )

    def generate_json(self, prompt: str) -> Any:
        last_error: Exception | None = None

        for attempt in range(1, self.retry_attempts + 1):
            try:
                logger.info("Groq API call attempt %s", attempt)

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a strict JSON API. "
                                "Return ONLY valid JSON. No explanation."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.1,
                    max_tokens=300,
                    response_format={"type": "json_object"},
                )

                content = response.choices[0].message.content or "{}"

                logger.info(" Raw Groq Response: %s", content)

                return _extract_json(content)

            except GroqServiceError as exc:
                last_error = exc
                logger.warning(
                    "Groq JSON validation failed attempt=%s/%s error=%s",
                    attempt,
                    self.retry_attempts,
                    exc,
                )

                if attempt < self.retry_attempts:
                    time.sleep(self.retry_backoff_seconds * attempt)

            except Exception as exc:
                last_error = exc
                logger.warning(
                    "Groq API attempt %s/%s failed: %s",
                    attempt,
                    self.retry_attempts,
                    exc,
                )

                if attempt < self.retry_attempts:
                    time.sleep(self.retry_backoff_seconds * attempt)

        raise GroqServiceError("Groq API call failed after retries") from last_error
