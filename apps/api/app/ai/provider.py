"""
Pluggable AI provider layer.

Usage:
    from app.ai.provider import get_ai_provider
    provider = get_ai_provider()
    reply = await provider.complete("Write a haiku about Redis queues")

Switch provider via .env: AI_PROVIDER=anthropic|openai|local
No other code needs to change when switching providers.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.config import get_settings


class AIProvider(ABC):
    """Common interface every provider implements."""

    @abstractmethod
    async def complete(self, prompt: str, *, system: str | None = None, max_tokens: int = 1024) -> str:
        """Return a single text completion for the given prompt."""
        raise NotImplementedError

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Return an embedding vector for the given text (for RAG)."""
        raise NotImplementedError


class AnthropicProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-5"):
        from anthropic import AsyncAnthropic
        self._client = AsyncAnthropic(api_key=api_key)
        self._model = model

    async def complete(self, prompt: str, *, system: str | None = None, max_tokens: int = 1024) -> str:
        response = await self._client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            system=system or "You are a helpful assistant.",
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in response.content if block.type == "text")

    async def embed(self, text: str) -> list[float]:
        # Anthropic has no native embeddings endpoint as of this writing.
        # Fall back to a local sentence-transformers model for embeddings
        # even when Anthropic is the completion provider.
        from app.ai.local_embeddings import embed_text
        return await embed_text(text)


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", embed_model: str = "text-embedding-3-small"):
        from openai import AsyncOpenAI
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model
        self._embed_model = embed_model

    async def complete(self, prompt: str, *, system: str | None = None, max_tokens: int = 1024) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system or "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content or ""

    async def embed(self, text: str) -> list[float]:
        response = await self._client.embeddings.create(model=self._embed_model, input=text)
        return response.data[0].embedding


class LocalProvider(AIProvider):
    """Talks to a local OpenAI-compatible server (e.g. Ollama, vLLM, LM Studio)."""

    def __init__(self, base_url: str, model: str = "llama3.1"):
        self._base_url = base_url.rstrip("/")
        self._model = model

    async def complete(self, prompt: str, *, system: str | None = None, max_tokens: int = 1024) -> str:
        import httpx
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f"{self._base_url}/api/chat",
                json={
                    "model": self._model,
                    "messages": [
                        {"role": "system", "content": system or "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    "stream": False,
                },
            )
            resp.raise_for_status()
            return resp.json()["message"]["content"]

    async def embed(self, text: str) -> list[float]:
        from app.ai.local_embeddings import embed_text
        return await embed_text(text)


def get_ai_provider() -> AIProvider:
    """Factory — returns the configured provider. This is the ONLY place
    that should branch on settings.ai_provider; everything else depends
    on the AIProvider interface, not on a specific vendor."""
    settings = get_settings()

    if settings.ai_provider == "anthropic":
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set but AI_PROVIDER=anthropic")
        return AnthropicProvider(settings.anthropic_api_key)

    if settings.ai_provider == "openai":
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not set but AI_PROVIDER=openai")
        return OpenAIProvider(settings.openai_api_key)

    if settings.ai_provider == "local":
        return LocalProvider(settings.local_model_url)

    raise ValueError(f"Unknown AI_PROVIDER: {settings.ai_provider!r}")
