from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    keycloak_id: str
    fio: str | None
    email: str | None
    role: str
    active: bool
    created_at: datetime


class UserUpdate(BaseModel):
    fio: str | None = None
    role: str | None = None
    active: bool | None = None


class AccessScopeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    university_id: uuid.UUID
    created_at: datetime


class AccessScopeCreate(BaseModel):
    university_id: uuid.UUID


class UserPage(BaseModel):
    items: list[UserOut]
    total: int
    limit: int
    offset: int
