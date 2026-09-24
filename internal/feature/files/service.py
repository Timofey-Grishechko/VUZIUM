from __future__ import annotations

from uuid import UUID

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from internal.core.errors import NotFoundError, ValidationError
from internal.core.logger import get_logger
from internal.feature.files import storage
from internal.feature.files.models import Attachment

logger = get_logger(__name__)

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB

# Разрешённые форматы из ТЗ, по расширению (mime от браузера часто врёт).
ALLOWED_EXTENSIONS: dict[str, str] = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "pdf": "application/pdf",
    "zip": "application/zip",
    "gz": "application/gzip",
    "gzip": "application/gzip",
    "rar": "application/vnd.rar",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


def _validate_extension(filename: str) -> str:
    if "." not in filename:
        raise ValidationError("File has no extension")
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"File extension .{ext} is not allowed",
            details={"allowed": sorted(ALLOWED_EXTENSIONS)},
        )
    return ext


async def upload_attachment(
    session: AsyncSession,
    *,
    file: UploadFile,
    entity: str,
    entity_id: str,
    uploaded_by: str | None,
) -> Attachment:
    if not file.filename:
        raise ValidationError("Filename is required")

    ext = _validate_extension(file.filename)
    content = await file.read()

    if not content:
        raise ValidationError("Uploaded file is empty")
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise ValidationError(
            f"File is too large (max {MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB)"
        )

    key = storage.build_object_key(file.filename)
    content_type = ALLOWED_EXTENSIONS[ext]
    await storage.upload_bytes(key, content, content_type)

    attachment = Attachment(
        filename=file.filename,
        mime=content_type,
        size=len(content),
        s3_key=key,
        entity=entity,
        entity_id=entity_id,
        uploaded_by=uploaded_by,
    )
    session.add(attachment)
    await session.commit()
    await session.refresh(attachment)

    logger.info(
        "File uploaded",
        extra={
            "ctx_attachment_id": str(attachment.id),
            "ctx_entity": entity,
            "ctx_entity_id": entity_id,
            "ctx_size": attachment.size,
        },
    )
    return attachment


async def get_attachment(session: AsyncSession, attachment_id: UUID) -> Attachment:
    obj = await session.get(Attachment, attachment_id)
    if obj is None:
        raise NotFoundError("Attachment not found")
    return obj


async def list_attachments(session: AsyncSession, *, entity: str, entity_id: str) -> list[Attachment]:
    result = await session.execute(
        select(Attachment)
        .where(Attachment.entity == entity, Attachment.entity_id == entity_id)
        .order_by(Attachment.created_at.desc())
    )
    return list(result.scalars().all())


async def delete_attachment(session: AsyncSession, attachment_id: UUID) -> None:
    attachment = await get_attachment(session, attachment_id)
    await storage.delete_object(attachment.s3_key)
    await session.delete(attachment)
    await session.commit()
