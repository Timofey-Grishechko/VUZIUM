import uuid

from fastapi import Request
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from internal.core import get_logger, set_request_id, set_user_id
from internal.core.security import decode_jwt

logger = get_logger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        set_request_id(request_id)

        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            try:
                payload = decode_jwt(auth.removeprefix("Bearer "))
                set_user_id(payload.get("sub"))
            except JWTError:
                logger.warning("Failed to decode bearer token", exc_info=True)

        logger.info(
            "Request started",
            extra={
                "ctx_method": request.method,
                "ctx_path": request.url.path,
            },
        )

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "Request finished",
            extra={"ctx_status_code": response.status_code},
        )
        return response