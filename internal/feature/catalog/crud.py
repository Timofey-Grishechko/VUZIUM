from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from internal.core.errors import ConflictError, NotFoundError


def _apply_filters(query, model: type, filters: dict[str, Any]):
    for column, value in filters.items():
        if value is None:
            continue
        col = getattr(model, column)
        if isinstance(value, str):
            query = query.where(col.ilike(f"%{value}%"))
        else:
            query = query.where(col == value)
    return query


async def list_paginated(
    session: AsyncSession,
    model: type,
    *,
    filters: dict[str, Any] | None = None,
    limit: int = 50,
    offset: int = 0,
    order_by=None,
) -> tuple[list, int]:
    filters = filters or {}

    query = _apply_filters(select(model), model, filters)
    count_query = _apply_filters(select(func.count()).select_from(model), model, filters)

    if order_by is not None:
        query = query.order_by(order_by)
    query = query.limit(limit).offset(offset)

    items = (await session.execute(query)).scalars().all()
    total = (await session.execute(count_query)).scalar_one()
    return list(items), total


async def get_or_404(session: AsyncSession, model: type, obj_id: UUID, message: str = "Not found"):
    obj = await session.get(model, obj_id)
    if obj is None:
        raise NotFoundError(message)
    return obj


async def create_obj(session: AsyncSession, model: type, **fields: Any):
    obj = model(**fields)
    session.add(obj)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ConflictError("Object with these unique fields already exists") from exc
    await session.refresh(obj)
    return obj


async def update_obj(session: AsyncSession, obj, **fields: Any):
    for key, value in fields.items():
        if value is not None:
            setattr(obj, key, value)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ConflictError("Update violates a unique constraint") from exc
    await session.refresh(obj)
    return obj


async def delete_obj(session: AsyncSession, obj) -> None:
    await session.delete(obj)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ConflictError("Cannot delete: object is referenced by other records") from exc
