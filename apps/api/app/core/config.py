"""Application configuration. All values overridable via .env / environment."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ── App ──────────────────────────────────────────────────────────────
    app_name: str = "Remarka"
    debug: bool = False

    # ── Database ─────────────────────────────────────────────────────────
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/remarka"

    # ── Redis / Celery ───────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # ── Object storage (S3-compatible: AWS S3 or Cloudflare R2) ─────────
    s3_endpoint_url: str | None = None          # e.g. https://<account>.r2.cloudflarestorage.com
    s3_access_key: str = ""
    s3_secret_key: str = ""
    s3_bucket: str = "remarka-artifacts"
    s3_region: str = "auto"

    # ── Vector store (RAG) ───────────────────────────────────────────────
    vector_backend: str = "qdrant"               # "qdrant" | "pgvector"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "remarka_documents"

    # ── AI provider (pluggable) ──────────────────────────────────────────
    ai_provider: str = "anthropic"               # "anthropic" | "openai" | "local"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    local_model_url: str = "http://localhost:11434"  # e.g. Ollama

    # ── News ──────────────────────────────────────────────────────────────
    news_user_agent: str = "RemarkaBot/1.0 (+https://remarka.example)"
    newsapi_key: str = ""                        # optional, phase 2

    @property
    def has_ai_provider_key(self) -> bool:
        if self.ai_provider == "anthropic":
            return bool(self.anthropic_api_key)
        if self.ai_provider == "openai":
            return bool(self.openai_api_key)
        return True  # local doesn't need a key


@lru_cache
def get_settings() -> Settings:
    return Settings()
