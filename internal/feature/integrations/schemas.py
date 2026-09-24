from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class IntegrationSourceIn(BaseModel):
    type: Literal["lms", "website"]
    name: str
    url: str
    api_key: str | None = None
    active: bool = True


class IntegrationSourceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: str
    name: str
    url: str
    active: bool
    created_at: datetime


class SyncLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source_id: uuid.UUID | None
    source_type: str
    status: str
    message: str | None
    items_synced: int
    created_at: datetime
