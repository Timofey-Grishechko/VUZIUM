from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ReportFilters(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    university_id: str | None = None
    direction_id: str | None = None
    product_id: str | None = None
    responsible_id: str | None = None
    status: str | None = None


class ReportCreate(BaseModel):
    format: Literal["xlsx", "pdf", "json"]
    filters: ReportFilters = ReportFilters()


class ReportStatusOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: str
    format: str
    status: str
    error: str | None
    created_by: str | None
    created_at: datetime
    finished_at: datetime | None
    download_url: str | None = None
