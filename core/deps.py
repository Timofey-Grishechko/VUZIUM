from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from internal.core.errors import ForbiddenError, UnauthorizedError
from internal.core.security import CurrentUser, decode_and_verify_token
from internal.feature.db.session import async_session_factory

bearer_scheme = HTTPBearer(auto_error=False)

BearerCreds = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]


async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(creds: BearerCreds) -> CurrentUser:
    if creds is None or not creds.credentials:
        raise UnauthorizedError("Missing bearer token")
    return await decode_and_verify_token(creds.credentials)


CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]


def require_roles(*roles: str):
    """Фабрика зависимостей: require_roles('admin', 'manager')."""

    async def _checker(user: CurrentUserDep) -> CurrentUser:
        if not any(r in user.roles for r in roles):
            raise ForbiddenError(
                "Insufficient permissions",
                details={"required": list(roles), "actual": user.roles},
            )
        return user

    return _checker


require_admin = require_roles("admin")
require_manager = require_roles("manager", "admin")
require_user = require_roles("user", "manager", "admin")