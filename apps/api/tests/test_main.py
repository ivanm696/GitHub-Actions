"""Tests for FastAPI endpoints — health checks, so CI actually verifies something."""
import os
import sys

# Ensure app package is importable when pytest runs from apps/api/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["app"] == "Remarka"


def test_readiness_reflects_missing_ai_key(monkeypatch):
    # With no API key configured, readiness should report 503, not crash.
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    monkeypatch.setenv("AI_PROVIDER", "anthropic")
    from app.core.config import get_settings
    get_settings.cache_clear()

    response = client.get("/health/ready")
    assert response.status_code == 503
    get_settings.cache_clear()
