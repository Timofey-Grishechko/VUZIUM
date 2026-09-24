"""
Инициализация Celery app.

Запуск:
    celery -A internal.feature.tasks.celery_app worker -l info
    celery -A internal.feature.tasks.celery_app beat -l info

Брокер/бэкенд берутся из internal.core.config.settings (уже настроено,
не трогаем). include перечисляет модули, в которых Backend-2/3 будут
объявлять @celery_app.task — модули сейчас пустые, это ок, Celery
просто не найдёт в них тасков до тех пор, пока они не появятся.
"""

from celery import Celery

from internal.core.config import settings
from internal.feature.tasks.schedules import BEAT_SCHEDULE

celery_app = Celery(
    "vuzium",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "internal.feature.reports.report",
        "internal.feature.integrations.integrations",
        "internal.feature.tasks.taks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    task_time_limit=15 * 60,
    task_soft_time_limit=10 * 60,
    worker_prefetch_multiplier=1,
    result_expires=60 * 60 * 24,
    beat_schedule=BEAT_SCHEDULE,
)
