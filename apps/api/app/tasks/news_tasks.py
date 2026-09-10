"""Background tasks — news fetching, scheduled via Celery beat."""
import asyncio

from app.core.celery_app import celery_app

# Configure real feeds here, or load from DB/config later.
DEFAULT_FEEDS = [
    "https://hnrss.org/frontpage",
]


@celery_app.task(name="app.tasks.news_tasks.fetch_all_feeds")
def fetch_all_feeds() -> dict:
    """Scheduled task: fetch all configured RSS feeds and store results."""
    from app.news.rss import fetch_all_feeds as _fetch_all_feeds

    items = asyncio.run(_fetch_all_feeds(DEFAULT_FEEDS))
    # TODO: persist `items` to the database once the News model exists.
    return {"fetched": len(items), "feeds": len(DEFAULT_FEEDS)}


@celery_app.task(name="app.tasks.news_tasks.fetch_single_feed")
def fetch_single_feed(feed_url: str) -> dict:
    from app.news.rss import fetch_feed

    items = asyncio.run(fetch_feed(feed_url))
    return {"feed": feed_url, "fetched": len(items)}
