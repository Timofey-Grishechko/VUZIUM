# app/core/security.py
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import httpx
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

from core.config import settings
from core.errors import UnauthorizedError
from core.logger import get_logger

logger = get_logger(__name__)


@dataclass
class _JWKSCache:
    keys: dict[str, Any] = field(default_factory=dict)
    fetched_at: float = 0.0
    ttl_sec: int = 3600

    def is_fresh(self) -> bool:
        return (time.time() - self.fetched_at) < self.ttl_sec


_jwks_cache = _JWKSCache()


async def _fetch_jwks() -> dict[str, Any]:
    """Скачивает JWKS (публичные ключи) из Keycloak."""
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(settings.keycloak_jwks_url)
        resp.raise_for_status()
        return resp.json()


async def _get_signing_key(kid: str) -> dict[str, Any]:
    """Returning public key by his kid"""
    if not _jwks_cache.is_fresh() or kid not in _jwks_cache.keys:
        try:
            jwks = await _fetch_jwks()
            _jwks_cache.keys = {k["kid"]: k for k in jwks.get("keys", [])}
            _jwks_cache.fetched_at = time.time()
            logger.info("JWKS refreshed", extra={"ctx_keys": len(_jwks_cache.keys)})
        except Exception:
            logger.exception("Failed to fetch JWKS")
            raise UnauthorizedError("Unable to verify token")

    key = _jwks_cache.keys.get(kid)
    if not key:
        raise UnauthorizedError("Signing key not found")
    return key


@dataclass
class CurrentUser:
    id: str                  
    username: str
    email: str | None
    roles: list[str]
    raw: dict[str, Any]

    @property
    def is_admin(self) -> bool:
        return "admin" in self.roles

    @property
    def is_manager(self) -> bool:
        return "manager" in self.roles or self.is_admin

    @property
    def is_user(self) -> bool:
        return "user" in self.roles or self.is_manager


async def decode_and_verify_token(token: str) -> CurrentUser:
    """Проверяет JWT от Keycloak и возвращает пользователя."""
    try:
        header = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise UnauthorizedError("Invalid token header") from exc

    kid = header.get("kid")
    if not kid:
        raise UnauthorizedError("Token missing kid")

    signing_key = await _get_signing_key(kid)

    try:
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=[settings.jwt_algorithm],
            issuer=settings.keycloak_issuer,
            audience=settings.keycloak_audience if settings.keycloak_verify_audience else None,
            options={
                "verify_aud": settings.keycloak_verify_audience,
                "verify_iss": True,
                "verify_exp": True,
            },
        )
    except ExpiredSignatureError as exc:
        raise UnauthorizedError("Token expired") from exc
    except JWTError as exc:
        logger.warning("JWT verification failed", extra={"ctx_error": str(exc)})
        raise UnauthorizedError("Invalid token") from exc

    realm_roles = payload.get("realm_access", {}).get("roles", [])
    client_roles = (
        payload.get("resource_access", {})
        .get(settings.keycloak_client_id, {})
        .get("roles", [])
    )
    roles = list({*realm_roles, *client_roles})

    return CurrentUser(
        id=payload["sub"],
        username=payload.get("preferred_username", ""),
        email=payload.get("email"),
        roles=roles,
        raw=payload,
    )


def hash_password(password: str) -> str:
    from passlib.context import CryptContext
    ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return ctx.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    from passlib.context import CryptContext
    ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return ctx.verify(password, hashed)


def has_any_role(user: CurrentUser, *roles: str) -> bool:
    return any(r in user.roles for r in roles)


def ensure_roles(user: CurrentUser, *roles: str) -> None:
    if not has_any_role(user, *roles):
        raise UnauthorizedError(
            "Insufficient permissions",
            code="FORBIDDEN",
            status_code=403,
        )