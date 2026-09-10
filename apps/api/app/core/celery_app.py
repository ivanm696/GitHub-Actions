"""Celery application — task queue backed by Redis."""
from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "remarka",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.tasks.news_tasks",
        "app.tasks.ai_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=60 * 10,       # hard limit: 10 min per task
    task_soft_time_limit=60 * 8,   # soft limit: 8 min
    worker_max_tasks_per_child=200,
)

celery_app.conf.beat_schedule = {
    "fetch-rss-every-30-minutes": {
        "task": "app.tasks.news_tasks.fetch_all_feeds",
        "schedule": 30 * 60,
    },
}
