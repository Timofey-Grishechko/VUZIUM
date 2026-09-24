from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from internal.core.logger import get_logger
from internal.feature.audit.models import AuditLog

logger = get_logger(__name__)


async def record(
    session: AsyncSession,
    *,
    action: str,
    entity: str,
    entity_id: str | None = None,
    user_id: str | None = None,
    username: str | None = None,
    method: str | None = None,
    path: str | None = None,
    status_code: int | None = None,
    payload: dict[str, Any] | None = None,
    commit: bool = True,
) -> AuditLog:
    """
    Записывает одно событие аудита.

    Вызывать явно из сервисов других фич в момент мутации (создание/
    изменение/удаление, переход этапа workflow и т.п.) — там известна
    конкретная сущность и её id, чего не знает общая middleware.

    commit=False позволяет включить audit-запись в ту же транзакцию,
    что и сама бизнес-операция: тогда сервис-вызывающий код сам должен
    вызвать session.commit(), и если бизнес-операция откатится — лог
    аудита откатится вместе с ней (это осознанный выбор, а не баг).
    """
    entry = AuditLog(
        user_id=user_id,
        username=username,
        action=action,
        entity=entity,
        entity_id=str(entity_id) if entity_id is not None else None,
        method=method,
        path=path,
        status_code=status_code,
        payload=payload,
    )
    session.add(entry)

    if commit:
        await session.commit()
        await session.refresh(entry)
    else:
        await session.flush()

    logger.info(
        "Audit event recorded",
        extra={
            "ctx_action": action,
            "ctx_entity": entity,
            "ctx_entity_id": entry.entity_id,
            "ctx_user_id": user_id,
        },
    )
    return entry


async def list_logs(
    session: AsyncSession,
    *,
    user_id: str | None = None,
    entity: str | None = None,
    action: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[AuditLog], int]:
    """Фильтрованный, постранично выданный список записей аудита, новые первыми."""
    query = select(AuditLog)
    count_query = select(func.count()).select_from(AuditLog)

    conditions = []
    if user_id:
        conditions.append(AuditLog.user_id == user_id)
    if entity:
        conditions.append(AuditLog.entity == entity)
    if action:
        conditions.append(AuditLog.action == action)
    if date_from:
        conditions.append(AuditLog.created_at >= date_from)
    if date_to:
        conditions.append(AuditLog.created_at <= date_to)

    for cond in conditions:
        query = query.where(cond)
        count_query = count_query.where(cond)

    query = query.order_by(AuditLog.created_at.desc()).limit(limit).offset(offset)

    result = await session.execute(query)
    items = list(result.scalars().all())

    total_result = await session.execute(count_query)
    total = total_result.scalar_one()

    return items, total
