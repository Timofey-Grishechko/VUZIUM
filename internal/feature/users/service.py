from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from internal.core.errors import ConflictError, NotFoundError
from internal.core.security import CurrentUser
from internal.feature.users.models import AccessScope, User


def _primary_role(user: CurrentUser) -> str:
    if user.is_admin:
        return "admin"
    if user.is_manager:
        return "manager"
    return "user"


async def get_or_create_from_token(session: AsyncSession, user: CurrentUser) -> User:
    """
    Upsert локального профиля по данным из проверенного JWT. Вызывается
    из зависимостей других роутеров (workflow/catalog), когда нужен
    users.id — не полагаемся на то, что пользователь явно "регистрировался".
    """
    result = await session.execute(select(User).where(User.keycloak_id == user.id))
    local = result.scalar_one_or_none()

    role = _primary_role(user)

    if local is None:
        local = User(keycloak_id=user.id, fio=user.username, email=user.email, role=role)
        session.add(local)
        try:
            await session.commit()
        except IntegrityError:
            # Параллельный запрос уже создал профиль — просто перечитываем.
            await session.rollback()
            result = await session.execute(select(User).where(User.keycloak_id == user.id))
            local = result.scalar_one()
        else:
            await session.refresh(local)
        return local

    changed = False
    if user.email and local.email != user.email:
        local.email = user.email
        changed = True
    if user.username and local.fio != user.username:
        local.fio = user.username
        changed = True
    if local.role != role:
        local.role = role
        changed = True

    if changed:
        await session.commit()
        await session.refresh(local)

    return local


async def list_users(session: AsyncSession, *, limit: int = 50, offset: int = 0) -> tuple[list[User], int]:
    result = await session.execute(select(User).order_by(User.created_at.desc()).limit(limit).offset(offset))
    items = list(result.scalars().all())
    total = (await session.execute(select(func.count()).select_from(User))).scalar_one()
    return items, total


async def get_user(session: AsyncSession, user_id: UUID) -> User:
    obj = await session.get(User, user_id)
    if obj is None:
        raise NotFoundError("User not found")
    return obj


async def update_user(session: AsyncSession, user_id: UUID, *, fio: str | None, role: str | None, active: bool | None) -> User:
    obj = await get_user(session, user_id)
    if fio is not None:
        obj.fio = fio
    if role is not None:
        obj.role = role
    if active is not None:
        obj.active = active
    await session.commit()
    await session.refresh(obj)
    return obj


async def list_access_scopes(session: AsyncSession, user_id: UUID) -> list[AccessScope]:
    result = await session.execute(select(AccessScope).where(AccessScope.user_id == user_id))
    return list(result.scalars().all())


async def add_access_scope(session: AsyncSession, user_id: UUID, university_id: UUID) -> AccessScope:
    await get_user(session, user_id)
    scope = AccessScope(user_id=user_id, university_id=university_id)
    session.add(scope)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ConflictError("Access scope already exists for this university") from exc
    await session.refresh(scope)
    return scope


async def remove_access_scope(session: AsyncSession, user_id: UUID, scope_id: UUID) -> None:
    scope = await session.get(AccessScope, scope_id)
    if scope is None or scope.user_id != user_id:
        raise NotFoundError("Access scope not found")
    await session.delete(scope)
    await session.commit()


async def get_accessible_university_ids(session: AsyncSession, user: CurrentUser) -> list[UUID] | None:
    """
    None означает доступ ко всем вузам (роль admin). Иначе — список id
    вузов из AccessScope пользователя (может быть пустым — значит доступа
    пока нет ни к одному вузу). Используется workflow/catalog для
    фильтрации выдачи по ролям manager/user.
    """
    if user.is_admin:
        return None

    local = await get_or_create_from_token(session, user)
    result = await session.execute(select(AccessScope.university_id).where(AccessScope.user_id == local.id))
    return [row[0] for row in result.all()]
