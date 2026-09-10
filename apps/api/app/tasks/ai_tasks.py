"""Background tasks — AI content generation (async work, runs in Celery worker)."""
import asyncio

from app.core.celery_app import celery_app


@celery_app.task(name="app.tasks.ai_tasks.generate_content")
def generate_content(prompt: str, system: str | None = None) -> dict:
    """Run a completion job on the configured AI provider in the background."""
    from app.ai.provider import get_ai_provider

    async def _run() -> str:
        provider = get_ai_provider()
        return await provider.complete(prompt, system=system)

    text = asyncio.run(_run())
    return {"prompt": prompt, "result": text}


@celery_app.task(name="app.tasks.ai_tasks.index_document")
def index_document(text: str, metadata: dict) -> dict:
    """Embed and store a document in the vector store (RAG ingestion)."""
    from app.rag.vector_store import upsert_document

    async def _run() -> str:
        return await upsert_document(text, metadata)

    point_id = asyncio.run(_run())
    return {"point_id": point_id}
