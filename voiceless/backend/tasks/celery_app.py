import sys
from pathlib import Path

# Ensure backend dir is on sys.path for forked worker processes
_backend_dir = str(Path(__file__).resolve().parent.parent)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from celery import Celery
from config import settings

celery = Celery(
    "voiceless",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,  # One task at a time (API rate limits)
)

celery.conf.update(
    include=[
        "tasks.produce_episode",
        "tasks.produce_moment",
        "tasks.discover_blogs",
    ]
)
