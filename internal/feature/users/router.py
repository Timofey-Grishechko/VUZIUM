from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query

from internal.core.deps import CurrentUserDep, DbSession, require_admin
from internal.feature.users import service
from internal.feature.users.schemas import AccessScopeCreate, AccessScopeOut, UserOut, UserPage, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
async def get_me(db: DbSession, user: CurrentUserDep) -> UserOut:
    local = await service.get_or_create_from_token(db, user)
    return UserOut.model_validate(local)


@router.get("", response_model=UserPage, dependencies=[Depends(require_admin)])
async def list_users(
    db: DbSession, limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)
) -> UserPage:
    items, total = await service.list_users(db, limit=limit, offset=offset)
    return UserPage(items=[UserOut.model_validate(i) for i in items], total=total, limit=limit, offset=offset)


@router.get("/{user_id}", response_model=UserOut, dependencies=[Depends(require_admin)])
async def get_user(user_id: uuid.UUID, db: DbSession) -> UserOut:
    return UserOut.model_validate(await service.get_user(db, user_id))


@router.patch("/{user_id}", response_model=UserOut, dependencies=[Depends(require_admin)])
async def update_user(user_id: uuid.UUID, payload: UserUpdate, db: DbSession) -> UserOut:
    obj = await service.update_user(db, user_id, fio=payload.fio, role=payload.role, active=payload.active)
    return UserOut.model_validate(obj)


@router.get("/{user_id}/access-scopes", response_model=list[AccessScopeOut], dependencies=[Depends(require_admin)])
async def list_access_scopes(user_id: uuid.UUID, db: DbSession) -> list[AccessScopeOut]:
    items = await service.list_access_scopes(db, user_id)
    return [AccessScopeOut.model_validate(i) for i in items]


@router.post(
    "/{user_id}/access-scopes", response_model=AccessScopeOut, status_code=201,
    dependencies=[Depends(require_admin)],
)
async def add_access_scope(user_id: uuid.UUID, payload: AccessScopeCreate, db: DbSession) -> AccessScopeOut:
    scope = await service.add_access_scope(db, user_id, payload.university_id)
    return AccessScopeOut.model_validate(scope)


@router.delete(
    "/{user_id}/access-scopes/{scope_id}", status_code=204, dependencies=[Depends(require_admin)],
)
async def remove_access_scope(user_id: uuid.UUID, scope_id: uuid.UUID, db: DbSession) -> None:
    await service.remove_access_scope(db, user_id, scope_id)
