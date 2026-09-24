from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from internal.feature.db.base import Base


class User(Base):
    """
    Локальный профиль пользователя. Источник истины по identity/ролям —
    всё равно JWT из Keycloak (core/security.py:CurrentUser); эта
    таблица нужна для FK (AccessScope, Workflow.manager_id, Stage.assignee_id)
    и для отображения ФИО/фильтров в UI. Синхронизируется upsert'ом при
    каждом первом обращении пользователя (см. service.get_or_create_from_token).
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    keycloak_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    fio: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Денормализованная "старшая" роль из токена — для удобных фильтров/списков.
    # Реальная авторизация всё равно идёт по ролям из JWT (require_admin/manager/user).
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="user")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class AccessScope(Base):
    """Ограничивает видимость данных для роли manager/user конкретными вузами."""

    __tablename__ = "access_scopes"
    __table_args__ = (UniqueConstraint("user_id", "university_id", name="uq_access_scope_user_university"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    university_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("universities.id", ondelete="CASCADE"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
