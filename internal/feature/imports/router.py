from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, UploadFile

from internal.core.deps import CurrentUserDep, DbSession, require_manager
from internal.feature.imports import service
from internal.feature.imports.mapping import TARGET_FIELDS
from internal.feature.imports.schemas import (
    CatalogImportOut,
    ImportReport,
    ImportUploadResponse,
    MappingIn,
    MappingOut,
)

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/xlsx", response_model=ImportUploadResponse, status_code=201)
async def upload_xlsx(
    db: DbSession,
    user: CurrentUserDep,
    file: UploadFile = File(...),
) -> ImportUploadResponse:
    record, columns = await service.start_import(db, file=file, user_id=user.id)
    return ImportUploadResponse(
        import_id=record.id,
        filename=record.filename,
        columns=columns,
        target_fields=TARGET_FIELDS,
    )


@router.post("/{import_id}/mapping", response_model=MappingOut)
async def set_mapping(
    import_id: uuid.UUID,
    payload: MappingIn,
    db: DbSession,
    user: CurrentUserDep,
) -> MappingOut:
    return await service.save_mapping(
        db, import_id=import_id, mapping=payload.mapping, created_by=user.id
    )


@router.post("/{import_id}/run", response_model=ImportReport, dependencies=[Depends(require_manager)])
async def run_import(import_id: uuid.UUID, db: DbSession) -> ImportReport:
    return await service.run_import(db, import_id=import_id)


@router.get("/{import_id}", response_model=CatalogImportOut)
async def get_import_status(import_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> CatalogImportOut:
    return await service.get_import(db, import_id)
