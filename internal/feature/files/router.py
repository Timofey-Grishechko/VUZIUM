from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile

from internal.core.deps import CurrentUserDep, DbSession, require_manager
from internal.feature.audit import service as audit_service
from internal.feature.files import service, storage
from internal.feature.files.schemas import AttachmentOut, AttachmentWithUrl

router = APIRouter(prefix="/files", tags=["files"])


@router.post("", response_model=AttachmentWithUrl, status_code=201)
async def upload_file(
    db: DbSession,
    user: CurrentUserDep,
    entity: str = Form(...),
    entity_id: str = Form(...),
    file: UploadFile = File(...),
) -> AttachmentWithUrl:
    attachment = await service.upload_attachment(
        db, file=file, entity=entity, entity_id=entity_id, uploaded_by=user.id
    )
    url = await storage.presigned_get_url(attachment.s3_key)

    await audit_service.record(
        db,
        action="upload",
        entity="attachment",
        entity_id=str(attachment.id),
        user_id=user.id,
        username=user.username,
        payload={"filename": attachment.filename, "target_entity": entity, "target_entity_id": entity_id},
    )

    return AttachmentWithUrl(**AttachmentOut.model_validate(attachment).model_dump(), download_url=url)


@router.get("", response_model=list[AttachmentOut])
async def list_files(db: DbSession, user: CurrentUserDep, entity: str, entity_id: str) -> list[AttachmentOut]:
    items = await service.list_attachments(db, entity=entity, entity_id=entity_id)
    return [AttachmentOut.model_validate(item) for item in items]


@router.get("/{attachment_id}", response_model=AttachmentWithUrl)
async def get_file(attachment_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> AttachmentWithUrl:
    attachment = await service.get_attachment(db, attachment_id)
    url = await storage.presigned_get_url(attachment.s3_key)
    return AttachmentWithUrl(**AttachmentOut.model_validate(attachment).model_dump(), download_url=url)


@router.delete("/{attachment_id}", status_code=204, dependencies=[Depends(require_manager)])
async def delete_file(attachment_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> None:
    await service.delete_attachment(db, attachment_id)
    await audit_service.record(
        db,
        action="delete",
        entity="attachment",
        entity_id=str(attachment_id),
        user_id=user.id,
        username=user.username,
    )
