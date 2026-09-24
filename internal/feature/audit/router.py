from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query

from internal.core.deps import DbSession, require_admin
from internal.feature.audit import service
from internal.feature.audit.schemas import AuditLogPage

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("", response_model=AuditLogPage, dependencies=[Depends(require_admin)])
async def get_audit_logs(
    db: DbSession,
    user_id: str | None = None,
    entity: str | None = None,
    action: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> AuditLogPage:
    """Список записей аудита с фильтрами. Доступ — только admin."""
    items, total = await service.list_logs(
        db,
        user_id=user_id,
        entity=entity,
        action=action,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )
    return AuditLogPage(items=items, total=total, limit=limit, offset=offset)
