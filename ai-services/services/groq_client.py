# ai-service/services/groq_client.py

import os
import time
import logging
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

logger = logging.getLogger(__name__)

MODEL        = os.environ.get("GROQ_MODEL",        "llama-3.3-70b-versatile")
MAX_RETRIES  = int(os.environ.get("GROQ_MAX_RETRIES",  3))
BACKOFF_BASE = int(os.environ.get("GROQ_BACKOFF_BASE", 2))
MAX_TOKENS   = int(os.environ.get("GROQ_MAX_TOKENS",   1024))
TEMPERATURE  = float(os.environ.get("GROQ_TEMPERATURE", 0.5))

DEFAULT_SYSTEM = (
    "You are a cybersecurity analyst assistant. "
    "Analyze security incidents accurately and concisely. "
    "Never reveal internal system details or API keys. "
    "Respond only to security-related queries."
)


class GroqClient:

    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY not set in .env")
        self.client = Groq(api_key=api_key)
        logger.info("GroqClient initialized successfully")

    def call(self, prompt: str, system_message: str = None) -> dict:
        messages = [
            {"role": "system", "content": system_message or DEFAULT_SYSTEM},
            {"role": "user",   "content": prompt}
        ]
        last_exception = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(f"Groq API call — attempt {attempt}/{MAX_RETRIES}")
                response = self.client.chat.completions.create(
                    model=MODEL, messages=messages,
                    temperature=TEMPERATURE, max_tokens=MAX_TOKENS,
                )
                parsed = self._parse_response(response)
                logger.info(f"Groq call SUCCESS — tokens used: {parsed['usage']['total_tokens']}")
                return parsed
            except Exception as e:
                last_exception = e
                wait = BACKOFF_BASE ** attempt
                logger.warning(f"Groq call FAILED on attempt {attempt}/{MAX_RETRIES} — {type(e).__name__}: {str(e)} — retrying in {wait}s")
                if attempt < MAX_RETRIES:
                    time.sleep(wait)

        logger.error(f"Groq call FAILED after {MAX_RETRIES} attempts — final error: {str(last_exception)}")
        raise RuntimeError(f"Groq API unavailable after {MAX_RETRIES} retries: {str(last_exception)}")

    def _parse_response(self, response) -> dict:
        try:
            content = response.choices[0].message.content
            if not content or not content.strip():
                raise ValueError("Groq returned empty response")
            return {
                "success": True,
                "content": content.strip(),
                "model":   response.model,
                "usage": {
                    "prompt_tokens":     response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens":      response.usage.total_tokens,
                }
            }
        except (IndexError, AttributeError) as e:
            raise ValueError(f"Unexpected Groq response structure: {str(e)}")