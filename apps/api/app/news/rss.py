"""
RSS feed fetcher — respects robots.txt before fetching each feed.

Phase 2 (not yet implemented): NewsAPI as an additional source once
NEWSAPI_KEY is set — see fetch_from_newsapi() stub below.
"""
from __future__ import annotations

import urllib.robotparser
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx

from app.core.config import get_settings

settings = get_settings()


@dataclass
class NewsItem:
    title: str
    link: str
    published: str | None
    summary: str | None
    source: str


def _robots_allows(url: str, user_agent: str) -> bool:
    """Check robots.txt for the given URL's domain before fetching it."""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception:
        # If robots.txt is unreachable, default to NOT fetching —
        # fail closed rather than assume permission.
        return False
    return rp.can_fetch(user_agent, url)


async def fetch_feed(feed_url: str) -> list[NewsItem]:
    """Fetch and parse a single RSS/Atom feed, after checking robots.txt."""
    import feedparser

    if not _robots_allows(feed_url, settings.news_user_agent):
        return []

    async with httpx.AsyncClient(
        headers={"User-Agent": settings.news_user_agent}, timeout=15
    ) as client:
        response = await client.get(feed_url)
        response.raise_for_status()

    parsed = feedparser.parse(response.text)
    domain = urlparse(feed_url).netloc

    items = []
    for entry in parsed.entries:
        items.append(
            NewsItem(
                title=entry.get("title", ""),
                link=entry.get("link", ""),
                published=entry.get("published", None),
                summary=entry.get("summary", None),
                source=domain,
            )
        )
    return items


async def fetch_all_feeds(feed_urls: list[str]) -> list[NewsItem]:
    """Fetch multiple feeds concurrently, skipping any that fail."""
    import asyncio

    results = await asyncio.gather(
        *(fetch_feed(url) for url in feed_urls), return_exceptions=True
    )
    items: list[NewsItem] = []
    for result in results:
        if isinstance(result, Exception):
            continue
        items.extend(result)
    return items


async def fetch_from_newsapi(query: str) -> list[NewsItem]:
    """
    Phase 2 stub. Enable once NEWSAPI_KEY is configured.
    https://newsapi.org/docs/endpoints/everything
    """
    if not settings.newsapi_key:
        raise RuntimeError("NEWSAPI_KEY not configured — this is a phase 2 feature")

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(
            "https://newsapi.org/v2/everything",
            params={"q": query, "apiKey": settings.newsapi_key},
        )
        response.raise_for_status()
        data = response.json()

    return [
        NewsItem(
            title=a["title"],
            link=a["url"],
            published=a.get("publishedAt"),
            summary=a.get("description"),
            source=a.get("source", {}).get("name", "newsapi"),
        )
        for a in data.get("articles", [])
    ]
