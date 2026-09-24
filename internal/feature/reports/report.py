"""
Точка входа фичи reports: celery-таски генерации/очистки отчётов
(имена "reports.generate" и "reports.cleanup_expired" — второе
совпадает с расписанием в tasks/schedules.py, оба уже входят в
include= у celery_app в tasks/celery_app.py, поэтому сам tasks/ не
трогаю) + реэкспорт router.
"""

from __future__ import annotations

import asyncio

from internal.core.logger import get_logger
from internal.feature.reports.router import router
from internal.feature.tasks.celery_app import celery_app

logger = get_logger(__name__)

__all__ = ["router", "generate_report_task"]


@celery_app.task(name="reports.generate", bind=True, max_retries=2)
def generate_report_task(self, report_id: str) -> str:
    try:
        return asyncio.run(_generate(report_id))
    except Exception as exc:
        logger.exception("reports.generate task failed", extra={"ctx_report_id": report_id})
        raise self.retry(exc=exc, countdown=10) from exc


async def _generate(report_id: str) -> str:
    from internal.feature.db.session import async_session_factory
    from internal.feature.reports import service

    async with async_session_factory() as session:
        await service.run_report_generation(session, report_id=report_id)
    return report_id


@celery_app.task(name="reports.cleanup_expired")
def cleanup_expired_reports_task() -> int:
    """
    Плейсхолдер: удаление файлов отчётов старше N дней из MinIO и
    простановка status="expired". Логику включить, когда определим
    политику хранения (сколько дней держим готовые файлы отчётов).
    """
    logger.info("cleanup_expired_reports_task: placeholder, no-op")
    return 0
