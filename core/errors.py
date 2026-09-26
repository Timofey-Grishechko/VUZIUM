from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from internal.core.context import get_request_id
from internal.core.logger import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    """Base domain excaptions"""

    code: str = "APP_ERROR"
    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = "Application error"

    def __init__(
        self,
        message: str | None = None,
        *,
        code: str | None = None,
        status_code: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.message
        self.code = code or self.code
        self.status_code = status_code or self.status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppError):
    code = "NOT_FOUND"
    status_code = status.HTTP_404_NOT_FOUND
    message = "Resource not found"


class ConflictError(AppError):
    code = "CONFLICT"
    status_code = status.HTTP_409_CONFLICT
    message = "Conflict"


class ValidationError(AppError):
    code = "VALIDATION_ERROR"
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Validation failed"


class UnauthorizedError(AppError):
    code = "UNAUTHORIZED"
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Unauthorized"


class ForbiddenError(AppError):
    code = "FORBIDDEN"
    status_code = status.HTTP_403_FORBIDDEN
    message = "Forbidden"


def _error_payload(
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "details": details or {},
        "request_id": get_request_id(),
    }


def register_exception_handlers(app: FastAPI) -> None:
    """Регистрирует обработчики ошибок. Вызвать в main.py."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        logger.warning(
            "AppError",
            extra={"ctx_code": exc.code, "ctx_path": request.url.path},
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_payload(exc.code, exc.message, exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        logger.warning(
            "Validation error",
            extra={"ctx_path": request.url.path, "ctx_errors": exc.errors()},
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_error_payload(
                "VALIDATION_ERROR",
                "Request validation failed",
                {"errors": exc.errors()},
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_payload(
                f"HTTP_{exc.status_code}",
                str(exc.detail),
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception):
        logger.exception("Unhandled error")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_error_payload(
                "INTERNAL_ERROR",
                "Internal server error",
            ),
        )