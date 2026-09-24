from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from internal.core.errors import NotFoundError, ValidationError
from internal.core.logger import get_logger
from internal.feature.files import storage
from internal.feature.imports import xlsx_parser
from internal.feature.imports.mapping import REQUIRED_FIELDS, validate_mapping
from internal.feature.imports.models import CatalogImport, ImportMapping
from internal.feature.imports.schemas import ImportReport

logger = get_logger(__name__)


async def start_import(
    session: AsyncSession, *, file: UploadFile, user_id: str | None
) -> tuple[CatalogImport, list[str]]:
    if not file.filename:
        raise ValidationError("Filename is required")

    content = await file.read()
    if not content:
        raise ValidationError("Uploaded file is empty")

    headers = xlsx_parser.read_headers(content)
    if not headers:
        raise ValidationError("Could not read header row from xlsx file")

    key = storage.build_object_key(file.filename)
    await storage.upload_bytes(
        key,
        content,
        file.content_type or "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    record = CatalogImport(filename=file.filename, s3_key=key, user_id=user_id)
    session.add(record)
    await session.commit()
    await session.refresh(record)

    logger.info(
        "Import uploaded",
        extra={"ctx_import_id": str(record.id), "ctx_columns": headers},
    )
    return record, headers


async def get_import(session: AsyncSession, import_id: UUID) -> CatalogImport:
    obj = await session.get(CatalogImport, import_id)
    if obj is None:
        raise NotFoundError("Import not found")
    return obj


async def save_mapping(
    session: AsyncSession, *, import_id: UUID, mapping: dict[str, str], created_by: str | None
) -> ImportMapping:
    validate_mapping(mapping)
    ci = await get_import(session, import_id)

    m = ImportMapping(name=f"import-{import_id}", mapping_json=mapping, created_by=created_by)
    session.add(m)
    await session.flush()

    ci.mapping_id = m.id
    ci.status = "mapped"

    await session.commit()
    await session.refresh(m)
    return m


def _validate_row(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        value = row.get(field)
        if value in (None, ""):
            errors.append(f"{field} is required")

    year = row.get("license_expires_year")
    if year not in (None, ""):
        try:
            int(year)
        except (TypeError, ValueError):
            errors.append("license_expires_year must be a number")

    signed_at = row.get("license_signed_at")
    if signed_at not in (None, "") and not isinstance(signed_at, (date, datetime)):
        errors.append("license_signed_at must be a date")

    return errors


async def _persist_row(session: AsyncSession, row: dict[str, Any]) -> None:
    """
    Заглушка сохранения валидной строки в каталог: get_or_create по
    University/Vendor/ITProduct + создание License появится здесь,
    когда Backend-2 сделает catalog/models.py. Формат row (по ключам
    из mapping.TARGET_FIELDS) уже финальный и меняться не должен.
    """
    logger.info("Import row validated and ready to persist", extra={"ctx_row": row})


async def run_import(session: AsyncSession, *, import_id: UUID) -> ImportReport:
    ci = await get_import(session, import_id)
    if ci.status != "mapped":
        raise ValidationError("Import has no mapping applied yet")
    if ci.mapping_id is None:
        raise ValidationError("Import has no mapping applied yet")

    mapping_obj = await session.get(ImportMapping, ci.mapping_id)
    if mapping_obj is None:
        raise NotFoundError("Mapping not found")

    content = await storage.download_bytes(ci.s3_key)
    raw_rows = xlsx_parser.read_rows(content)

    source_by_target: dict[str, str] = mapping_obj.mapping_json

    errors: list[dict[str, Any]] = []
    valid_rows: list[dict[str, Any]] = []

    for i, raw in enumerate(raw_rows, start=2):  # 1 — заголовок, данные со 2-й строки
        mapped_row = {target: raw.get(source) for target, source in source_by_target.items()}
        row_errors = _validate_row(mapped_row)
        if row_errors:
            errors.append({"row": i, "errors": row_errors})
        else:
            valid_rows.append(mapped_row)

    for row in valid_rows:
        await _persist_row(session, row)

    ci.total_rows = len(raw_rows)
    ci.error_rows = len(errors)
    ci.finished_at = datetime.now(timezone.utc)
    if errors and not valid_rows:
        ci.status = "failed"
    elif errors:
        ci.status = "done_with_errors"
    else:
        ci.status = "done"

    await session.commit()
    await session.refresh(ci)

    return ImportReport(
        import_id=ci.id,
        total=len(raw_rows),
        imported=len(valid_rows),
        failed=len(errors),
        errors=errors,
    )
