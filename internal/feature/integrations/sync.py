from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from internal.core.logger import get_logger

logger = get_logger(__name__)


def map_lms_item_to_workflow_payload(item: dict[str, Any]) -> dict[str, Any]:
    """
    Маппинг одного элемента ответа LMS в поля Workflow. Точные ключи
    ответа LMS уточнить с их API — пока используются правдоподобные
    предположения (university_id/course_id/status), поправить при
    реальной интеграции.
    """
    return {
        "external_id": item.get("id"),
        "university_id": item.get("university_id") or item.get("org_id"),
        "product_id": item.get("course_id") or item.get("product_id"),
        "status": item.get("status", "new"),
    }


def map_website_item_to_workflow_payload(item: dict[str, Any]) -> dict[str, Any]:
    """Аналогично map_lms_item_to_workflow_payload, но для заявок с сайта."""
    return {
        "external_id": item.get("id"),
        "university_id": item.get("university_id"),
        "product_id": item.get("product_id"),
        "status": item.get("status", "new"),
    }


async def apply_workflow_payload(session: AsyncSession, payload: dict[str, Any]) -> bool:
    """
    Создаёт/обновляет Workflow по данным из внешней системы (upsert по
    external_id). Возвращает True, если запись применена.

    Workflow-модель ещё не реализована (Backend-3) — пока просто
    логирует и возвращает False, ничего не ломая. Как только появится
    workflow/models.py, реализовать здесь upsert по external_id.
    """
    try:
        from internal.feature.workflow.models import Workflow  # type: ignore  # noqa: F401
    except ImportError:
        logger.warning("Workflow model not available yet, skipping sync payload", extra={"ctx_payload": payload})
        return False

    # TODO: upsert Workflow по payload["external_id"], когда появится модель
    return False
