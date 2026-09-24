from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from internal.core.logger import get_logger

logger = get_logger(__name__)

REPORT_COLUMNS = ["university", "direction", "product", "status", "responsible"]


async def build_dataset(
    session: AsyncSession,
    *,
    date_from: date | None = None,
    date_to: date | None = None,
    university_id: str | None = None,
    direction_id: str | None = None,
    product_id: str | None = None,
    responsible_id: str | None = None,
    status: str | None = None,
) -> list[dict[str, Any]]:
    """
    Собирает строки отчёта по фильтрам (период, вуз, направление, продукт,
    ответственный, статус).

    Workflow-модель ещё не реализована (Backend-3) — делаем best-effort
    импорт и, если её нет, возвращаем пустой датасет. Сам пайплайн отчёта
    (xlsx/pdf/json + графики + Celery-таск) уже полностью рабочий и не
    потребует переписывания, когда Workflow появится: достаточно будет
    реализовать только тело этой функции.
    """
    try:
        from internal.feature.workflow.models import Workflow  # type: ignore
    except ImportError:
        logger.warning("Workflow model not available yet, returning empty report dataset")
        return []

    query = select(Workflow)
    if university_id:
        query = query.where(Workflow.university_id == university_id)
    if direction_id:
        query = query.where(Workflow.direction_id == direction_id)
    if product_id:
        query = query.where(Workflow.product_id == product_id)
    if status:
        query = query.where(Workflow.status == status)
    if date_from:
        query = query.where(Workflow.created_at >= date_from)
    if date_to:
        query = query.where(Workflow.created_at <= date_to)
    if responsible_id and hasattr(Workflow, "responsible_id"):
        query = query.where(Workflow.responsible_id == responsible_id)

    result = await session.execute(query)
    rows = result.scalars().all()

    dataset: list[dict[str, Any]] = []
    for wf in rows:
        dataset.append(
            {
                "university": getattr(wf, "university_name", None) or str(getattr(wf, "university_id", "")),
                "direction": getattr(wf, "direction_name", None) or str(getattr(wf, "direction_id", "")),
                "product": getattr(wf, "product_name", None) or str(getattr(wf, "product_id", "")),
                "status": wf.status,
                "responsible": getattr(wf, "responsible_name", None) or "",
            }
        )
    return dataset
