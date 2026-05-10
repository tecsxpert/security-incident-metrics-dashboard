from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("GROQ_API_KEY", "test-api-key")
os.environ.setdefault("REDIS_CACHE_ENABLED", "false")
os.environ.setdefault("REDIS_URL", "memory://")
os.environ.setdefault("AI_RESPONSE_TIMEOUT_SECONDS", "1.8")


@pytest.fixture()
def app():
    from app import create_app

    flask_app = create_app()
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def incident_payload():
    return {
        "title": "Suspicious VPN Login",
        "description": "Multiple failed login attempts followed by a successful login from an unknown IP.",
    }


@pytest.fixture(autouse=True)
def synchronous_timeout(monkeypatch):
    import routes.describe as describe_route
    import routes.recommend as recommend_route
    import routes.report as report_route

    def run_now(operation, fallback):
        return operation()

    monkeypatch.setattr(describe_route, "run_with_timeout", run_now)
    monkeypatch.setattr(recommend_route, "run_with_timeout", run_now)
    monkeypatch.setattr(report_route, "run_with_timeout", run_now)
