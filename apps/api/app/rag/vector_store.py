"""Qdrant-backed vector store for retrieval-augmented generation (RAG)."""
from __future__ import annotations

import uuid
from functools import lru_cache

from app.core.config import get_settings


@lru_cache
def get_qdrant_client():
    from qdrant_client import QdrantClient
    settings = get_settings()
    return QdrantClient(url=settings.qdrant_url)


def ensure_collection(vector_size: int = 384) -> None:
    """Create the collection if it doesn't exist yet. Idempotent."""
    from qdrant_client.models import Distance, VectorParams

    settings = get_settings()
    client = get_qdrant_client()
    existing = {c.name for c in client.get_collections().collections}
    if settings.qdrant_collection not in existing:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


async def upsert_document(text: str, metadata: dict) -> str:
    """Embed `text` and store it with `metadata`. Returns the point id."""
    from app.ai.provider import get_ai_provider
    from qdrant_client.models import PointStruct

    settings = get_settings()
    provider = get_ai_provider()
    vector = await provider.embed(text)

    ensure_collection(vector_size=len(vector))

    point_id = str(uuid.uuid4())
    client = get_qdrant_client()
    client.upsert(
        collection_name=settings.qdrant_collection,
        points=[PointStruct(id=point_id, vector=vector, payload={"text": text, **metadata})],
    )
    return point_id


async def search(query: str, top_k: int = 5) -> list[dict]:
    """Semantic search — returns top_k matching documents with their scores."""
    from app.ai.provider import get_ai_provider

    settings = get_settings()
    provider = get_ai_provider()
    query_vector = await provider.embed(query)

    client = get_qdrant_client()
    results = client.search(
        collection_name=settings.qdrant_collection,
        query_vector=query_vector,
        limit=top_k,
    )
    return [{"score": r.score, **r.payload} for r in results]
