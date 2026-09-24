from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from internal.core.config import settings
from internal.core.logger import get_logger
from internal.core.security import decode_and_verify_token
from internal.feature.audit import service as audit_service
from internal.feature.db.session import async_session_factory

logger = get_logger(__name__)

_MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

# Не пишем как бизнес-события: health-check, доки, сам аудит-лог (иначе
# GET /audit будет плодить сам себя из-за других мутирующих запросов рядом).
_EXCLUDED_PREFIXES = (
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    f"{settings.api_v1_prefix}/audit",
)


class AuditMiddleware(BaseHTTPMiddleware):
    """
    Универсальный fallback-аудит на уровне HTTP: логирует сам факт
    мутирующего запроса (кто по токену, каким методом, на какой путь,
    с каким статусом ответа) — даже если конкретный сервис-фича не
    вызвал audit.service.record() с деталями сущности явно.

    Не подключена автоматически — captain должен добавить в main.py:

        from internal.feature.audit.middleware import AuditMiddleware
        app.add_middleware(AuditMiddleware)

    (сознательно не трогаю main.py в этой задаче).
    """

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        if request.method not in _MUTATING_METHODS:
            return response
        if request.url.path.startswith(_EXCLUDED_PREFIXES):
            return response

        user_id: str | None = None
        username: str | None = None
        auth_header = request.headers.get("authorization", "")
        if auth_header.lower().startswith("bearer "):
            try:
                user = await decode_and_verify_token(auth_header[7:])
                user_id, username = user.id, user.username
            except Exception:
                # Невалидный/просроченный токен уже приведёт к 401 на самом
                # роуте (это отработает auth-слой) — для аудита просто не
                # знаем, кто автор запроса.
                pass

        try:
            async with async_session_factory() as session:
                await audit_service.record(
                    session,
                    action=request.method.lower(),
                    entity="http_request",
                    entity_id=None,
                    user_id=user_id,
                    username=username,
                    method=request.method,
                    path=request.url.path,
                    status_code=response.status_code,
                    payload=None,
                )
        except Exception:
            # Аудит не должен уронить запрос пользователю.
            logger.exception("Failed to write audit log")

        return response
