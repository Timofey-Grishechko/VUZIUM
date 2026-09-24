"""
Точка входа фичи integrations: celery-таски "integrations.sync_lms" /
"integrations.sync_website" (имена совпадают с расписанием в
tasks/schedules.py, оба уже в include= у celery_app в
tasks/celery_app.py, поэтому сам tasks/ не трогаю) + реэкспорт router.
"""

from __future__ import annotations

import asyncio

from internal.core.logger import get_logger
from internal.feature.integrations.router import router
from internal.feature.tasks.celery_app import celery_app

logger = get_logger(__name__)

__all__ = ["router"]


@celery_app.task(name="integrations.sync_lms", bind=True, max_retries=2)
def sync_lms_task(self) -> str:
    try:
        return asyncio.run(_run_lms_sync())
    except Exception as exc:
        logger.exception("integrations.sync_lms task failed")
        raise self.retry(exc=exc, countdown=30) from exc


@celery_app.task(name="integrations.sync_website", bind=True, max_retries=2)
def sync_website_task(self) -> str:
    try:
        return asyncio.run(_run_website_sync())
    except Exception as exc:
        logger.exception("integrations.sync_website task failed")
        raise self.retry(exc=exc, countdown=30) from exc


async def _run_lms_sync() -> str:
    from internal.feature.db.session import async_session_factory
    from internal.feature.integrations import service

    async with async_session_factory() as session:
        log = await service.run_lms_sync(session)
        return str(log.id)


async def _run_website_sync() -> str:
    from internal.feature.db.session import async_session_factory
    from internal.feature.integrations import service

    async with async_session_factory() as session:
        log = await service.run_website_sync(session)
        return str(log.id)
