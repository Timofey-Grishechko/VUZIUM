from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttachmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    filename: str
    mime: str
    size: int
    entity: str
    entity_id: str
    uploaded_by: str | None
    created_at: datetime


class AttachmentWithUrl(AttachmentOut):
    download_url: str
