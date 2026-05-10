from __future__ import annotations

import sys
import types


def test_groq_service_uses_openai_compatible_messages(monkeypatch):
    captured = {}

    class FakeMessage:
        content = '{"summary":"ok","severity":"low"}'

    class FakeChoice:
        message = FakeMessage()

    class FakeResponse:
        choices = [FakeChoice()]

    class FakeCompletions:
        def create(self, **kwargs):
            captured.update(kwargs)
            return FakeResponse()

    class FakeChat:
        completions = FakeCompletions()

    class FakeGroq:
        def __init__(self, **kwargs):
            captured["client_kwargs"] = kwargs
            self.chat = FakeChat()

    fake_module = types.SimpleNamespace(Groq=FakeGroq)
    monkeypatch.setitem(sys.modules, "groq", fake_module)
    monkeypatch.setenv("GROQ_API_KEY", "test-api-key")
    monkeypatch.setenv("GROQ_RETRY_ATTEMPTS", "1")

    from services.groq_service import GroqService

    result = GroqService().generate_json("Summarize this incident.")

    assert result == {"summary": "ok", "severity": "low"}
    assert captured["model"] == "llama-3.3-70b-versatile"
    assert captured["messages"][0]["role"] == "system"
    assert captured["messages"][1] == {
        "role": "user",
        "content": "Summarize this incident.",
    }
    assert captured["response_format"] == {"type": "json_object"}


def test_cache_key_is_stable_for_same_input_order():
    from services.cache_service import build_cache_key

    key_a = build_cache_key("describe", {"title": "A", "description": "B"})
    key_b = build_cache_key("describe", {"description": "B", "title": "A"})

    assert key_a == key_b
    assert key_a.startswith("ai-service:describe:")
    assert len(key_a.rsplit(":", maxsplit=1)[-1]) == 64


def test_recommendation_normalizer_always_returns_three_items():
    from services.recommend_service import normalize_recommendations

    result = normalize_recommendations(
        {
            "recommendations": [
                {
                    "action_type": "Containment",
                    "description": "Isolate the affected endpoint.",
                    "priority": "HIGH",
                }
            ]
        }
    )

    assert len(result) == 3
    assert result[0] == {
        "action_type": "containment",
        "description": "Isolate the affected endpoint.",
        "priority": "high",
    }
