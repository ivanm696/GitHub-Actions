"""Tests for the pluggable AI provider factory."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from app.ai.provider import AnthropicProvider, LocalProvider, OpenAIProvider, get_ai_provider
from app.core.config import get_settings


def test_get_ai_provider_anthropic(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-key")
    get_settings.cache_clear()

    provider = get_ai_provider()
    assert isinstance(provider, AnthropicProvider)
    get_settings.cache_clear()


def test_get_ai_provider_openai(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    get_settings.cache_clear()

    provider = get_ai_provider()
    assert isinstance(provider, OpenAIProvider)
    get_settings.cache_clear()


def test_get_ai_provider_local_needs_no_key(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "local")
    get_settings.cache_clear()

    provider = get_ai_provider()
    assert isinstance(provider, LocalProvider)
    get_settings.cache_clear()


def test_get_ai_provider_missing_key_raises(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    get_settings.cache_clear()

    with pytest.raises(RuntimeError):
        get_ai_provider()
    get_settings.cache_clear()


def test_get_ai_provider_unknown_raises(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "not-a-real-provider")
    get_settings.cache_clear()

    with pytest.raises(ValueError):
        get_ai_provider()
    get_settings.cache_clear()
