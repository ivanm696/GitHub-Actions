"""
Local embeddings fallback (sentence-transformers) — used by providers
that don't offer a native embeddings endpoint (Anthropic, local LLMs).

Loaded lazily so importing this module has no cost if RAG isn't used.
"""
from functools import lru_cache


@lru_cache
def _get_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


async def embed_text(text: str) -> list[float]:
    model = _get_model()
    vector = model.encode(text, normalize_embeddings=True)
    return vector.tolist()
