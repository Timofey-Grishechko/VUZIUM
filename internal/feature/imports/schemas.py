from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ImportUploadResponse(BaseModel):
    import_id: uuid.UUID
    filename: str
    columns: list[str]
    target_fields: dict[str, str]


class MappingIn(BaseModel):
    mapping: dict[str, str]  # target_field -> имя колонки в файле


class MappingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    mapping_json: dict[str, str]
    created_by: str | None
    created_at: datetime


class CatalogImportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    filename: str
    status: str
    total_rows: int
    error_rows: int
    created_at: datetime
    finished_at: datetime | None


class ImportReport(BaseModel):
    import_id: uuid.UUID
    total: int
    imported: int
    failed: int
    errors: list[dict[str, Any]]
