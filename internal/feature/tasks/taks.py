"""
Health-check таск: подтверждает, что worker и брокер (Redis) живы.

Проверка вручную:
    from internal.feature.tasks.taks import ping
    ping.delay()
    # или из shell: celery -A internal.feature.tasks.celery_app call tasks.ping
"""

from internal.core.logger import get_logger
from internal.feature.tasks.celery_app import celery_app

logger = get_logger(__name__)


@celery_app.task(name="tasks.ping")
def ping() -> str:
    logger.info("Celery ping task executed")
    return "pong"
