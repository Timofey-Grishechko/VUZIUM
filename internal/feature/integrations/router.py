from __future__ import annotations

from fastapi import APIRouter, Depends

from internal.core.deps import DbSession, require_admin, require_manager
from internal.feature.integrations import service
from internal.feature.integrations.schemas import IntegrationSourceIn, IntegrationSourceOut, SyncLogOut

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.post(
    "/sources", response_model=IntegrationSourceOut, status_code=201,
    dependencies=[Depends(require_admin)],
)
async def create_source(payload: IntegrationSourceIn, db: DbSession) -> IntegrationSourceOut:
    return await service.create_source(db, payload)


@router.get("/sources", response_model=list[IntegrationSourceOut], dependencies=[Depends(require_manager)])
async def list_sources(db: DbSession, type: str | None = None) -> list[IntegrationSourceOut]:  # noqa: A002
    return await service.list_sources(db, source_type=type)


@router.post("/lms/sync", response_model=SyncLogOut, dependencies=[Depends(require_manager)])
async def sync_lms(db: DbSession) -> SyncLogOut:
    return await service.run_lms_sync(db)


@router.post("/website/sync", response_model=SyncLogOut, dependencies=[Depends(require_manager)])
async def sync_website(db: DbSession) -> SyncLogOut:
    return await service.run_website_sync(db)


@router.get("/sync-logs", response_model=list[SyncLogOut], dependencies=[Depends(require_manager)])
async def get_sync_logs(db: DbSession, limit: int = 50) -> list[SyncLogOut]:
    return await service.list_sync_logs(db, limit=limit)
