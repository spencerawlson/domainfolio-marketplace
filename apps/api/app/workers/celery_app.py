"""Celery worker skeleton. Tasks land per P0 stage; the app object and
broker wiring exist now so the stage work has a place to go.

Queues (planned): verification (DNS checks, re-verification),
escrow (status sync), notifications (email), search (index sync).
"""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "domainfolio",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.workers.*": {"queue": "default"},
    },
)


@celery_app.task(name="app.workers.health.ping")
def ping() -> str:
    return "pong"
