from __future__ import annotations

from typing import Literal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from internal.core.errors import NotFoundError
from internal.core.logger import get_logger
from internal.feature.integrations import sync as sync_mapper
from internal.feature.integrations.clients.lms import LMSClient
from internal.feature.integrations.clients.website import WebsiteClient
from internal.feature.integrations.models import IntegrationSource, SyncLog
from internal.feature.integrations.schemas import IntegrationSourceIn

logger = get_logger(__name__)


async def create_source(session: AsyncSession, payload: IntegrationSourceIn) -> IntegrationSource:
    source = IntegrationSource(**payload.model_dump())
    session.add(source)
    await session.commit()
    await session.refresh(source)
    return source


async def list_sources(session: AsyncSession, *, source_type: str | None = None) -> list[IntegrationSource]:
    query = select(IntegrationSource)
    if source_type:
        query = query.where(IntegrationSource.type == source_type)
    result = await session.execute(query.order_by(IntegrationSource.created_at.desc()))
    return list(result.scalars().all())


async def _get_active_sources(session: AsyncSession, source_type: str) -> list[IntegrationSource]:
    result = await session.execute(
        select(IntegrationSource).where(
            IntegrationSource.type == source_type,
            IntegrationSource.active.is_(True),
        )
    )
    return list(result.scalars().all())


async def _write_log(
    session: AsyncSession,
    *,
    source_id: UUID | None,
    source_type: str,
    status: str,
    message: str | None,
    items_synced: int,
) -> SyncLog:
    log = SyncLog(
        source_id=source_id,
        source_type=source_type,
        status=status,
        message=message,
        items_synced=items_synced,
    )
    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log


async def run_lms_sync(session: AsyncSession) -> SyncLog:
    sources = await _get_active_sources(session, "lms")
    if not sources:
        return await _write_log(
            session, source_id=None, source_type="lms", status="failed",
            message="No active LMS sources configured", items_synced=0,
        )

    total_applied = 0
    errors: list[str] = []
    for source in sources:
        client = LMSClient(source.url, source.api_key)
        try:
            items = await client.fetch_enrollments()
        except Exception as exc:  # noqa: BLE001
            logger.exception("LMS fetch failed", extra={"ctx_source": source.name})
            errors.append(f"{source.name}: {exc}")
            continue

        for item in items:
            payload = sync_mapper.map_lms_item_to_workflow_payload(item)
            if await sync_mapper.apply_workflow_payload(session, payload):
                total_applied += 1

    status: Literal["success", "partial", "failed"] = (
        "success" if not errors else ("partial" if total_applied else "failed")
    )
    return await _write_log(
        session,
        source_id=sources[0].id if len(sources) == 1 else None,
        source_type="lms",
        status=status,
        message="; ".join(errors) or None,
        items_synced=total_applied,
    )


async def run_website_sync(session: AsyncSession) -> SyncLog:
    sources = await _get_active_sources(session, "website")
    if not sources:
        return await _write_log(
            session, source_id=None, source_type="website", status="failed",
            message="No active website sources configured", items_synced=0,
        )

    total_applied = 0
    errors: list[str] = []
    for source in sources:
        client = WebsiteClient(source.url, source.api_key)
        try:
            items = await client.fetch_orders()
        except Exception as exc:  # noqa: BLE001
            logger.exception("Website fetch failed", extra={"ctx_source": source.name})
            errors.append(f"{source.name}: {exc}")
            continue

        for item in items:
            payload = sync_mapper.map_website_item_to_workflow_payload(item)
            if await sync_mapper.apply_workflow_payload(session, payload):
                total_applied += 1

    status = "success" if not errors else ("partial" if total_applied else "failed")
    return await _write_log(
        session,
        source_id=sources[0].id if len(sources) == 1 else None,
        source_type="website",
        status=status,
        message="; ".join(errors) or None,
        items_synced=total_applied,
    )


async def list_sync_logs(session: AsyncSession, *, limit: int = 50) -> list[SyncLog]:
    result = await session.execute(
        select(SyncLog).order_by(SyncLog.created_at.desc()).limit(limit)
    )
    return list(result.scalars().all())


async def get_source(session: AsyncSession, source_id: UUID) -> IntegrationSource:
    obj = await session.get(IntegrationSource, source_id)
    if obj is None:
        raise NotFoundError("Integration source not found")
    return obj
