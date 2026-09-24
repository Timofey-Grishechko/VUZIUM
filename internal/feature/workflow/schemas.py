from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int


class WorkflowCreate(BaseModel):
    university_id: uuid.UUID
    direction_id: uuid.UUID | None = None
    product_id: uuid.UUID | None = None
    manager_id: uuid.UUID | None = None


class WorkflowOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    university_id: uuid.UUID
    direction_id: uuid.UUID | None
    product_id: uuid.UUID | None
    manager_id: uuid.UUID | None
    status: str
    created_at: datetime
    updated_at: datetime


class StageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workflow_id: uuid.UUID
    order: int
    name: str
    status: str
    assignee_id: uuid.UUID | None
    deadline: date | None
    comment: str | None


class WorkflowDetailOut(WorkflowOut):
    stages: list[StageOut] = []


class StageTransitionIn(BaseModel):
    to_status: str
    comment: str | None = None


class StageTransitionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    stage_id: uuid.UUID
    from_status: str | None
    to_status: str
    user_id: str | None
    comment: str | None
    created_at: datetime


class StageRename(BaseModel):
    name: str | None = None
    order: int | None = None
