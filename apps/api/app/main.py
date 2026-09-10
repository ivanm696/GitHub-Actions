"""FastAPI application — Remarka API."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health() -> dict:
    """Liveness probe — used by CI and orchestration."""
    return {"status": "ok", "app": settings.app_name}


@app.get("/health/ready")
async def readiness() -> dict:
    """Readiness probe — checks that an AI provider key is configured."""
    if not settings.has_ai_provider_key:
        raise HTTPException(
            status_code=503,
            detail=f"AI provider '{settings.ai_provider}' is not configured (missing API key)",
        )
    return {"status": "ready", "ai_provider": settings.ai_provider}


# ── AI completion ────────────────────────────────────────────────────────

class CompletionRequest(BaseModel):
    prompt: str
    system: str | None = None
    max_tokens: int = 1024


class CompletionResponse(BaseModel):
    result: str
    provider: str


@app.post("/ai/complete", response_model=CompletionResponse)
async def complete(payload: CompletionRequest) -> CompletionResponse:
    from app.ai.provider import get_ai_provider

    provider = get_ai_provider()
    result = await provider.complete(payload.prompt, system=payload.system, max_tokens=payload.max_tokens)
    return CompletionResponse(result=result, provider=settings.ai_provider)


# ── RAG search ───────────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/rag/search")
async def rag_search(payload: SearchRequest) -> dict:
    from app.rag.vector_store import search

    results = await search(payload.query, top_k=payload.top_k)
    return {"query": payload.query, "results": results}


class IndexRequest(BaseModel):
    text: str
    metadata: dict = {}


@app.post("/rag/index")
async def rag_index(payload: IndexRequest) -> dict:
    """Queue a document for embedding + indexing (runs in Celery worker)."""
    from app.tasks.ai_tasks import index_document

    task = index_document.delay(payload.text, payload.metadata)
    return {"task_id": task.id, "status": "queued"}


# ── News ─────────────────────────────────────────────────────────────────

@app.post("/news/fetch")
async def trigger_news_fetch() -> dict:
    """Queue a news-fetch job (runs in Celery worker, respects robots.txt)."""
    from app.tasks.news_tasks import fetch_all_feeds

    task = fetch_all_feeds.delay()
    return {"task_id": task.id, "status": "queued"}


# ── Task status (generic) ────────────────────────────────────────────────

@app.get("/tasks/{task_id}")
async def task_status(task_id: str) -> dict:
    from app.core.celery_app import celery_app

    result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
