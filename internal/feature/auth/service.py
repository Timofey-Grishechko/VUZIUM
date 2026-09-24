from __future__ import annotations

from typing import Any

import httpx

from internal.core.config import settings
from internal.core.errors import UnauthorizedError
from internal.core.logger import get_logger

logger = get_logger(__name__)


async def login(username: str, password: str) -> dict[str, Any]:
    """
    Resource Owner Password Credentials grant — прокси до Keycloak,
    чтобы клиентам (мобильным/скриптам) не обязательно было тащить
    keycloak-js. Requires that Keycloak client has "Direct Access
    Grants" enabled.
    """
    data = {
        "grant_type": "password",
        "client_id": settings.keycloak_client_id,
        "client_secret": settings.keycloak_client_secret,
        "username": username,
        "password": password,
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(settings.keycloak_token_url, data=data)

    if resp.status_code != 200:
        logger.warning("Keycloak login failed", extra={"ctx_status": resp.status_code})
        raise UnauthorizedError("Invalid username or password")

    return resp.json()


async def refresh(refresh_token: str) -> dict[str, Any]:
    data = {
        "grant_type": "refresh_token",
        "client_id": settings.keycloak_client_id,
        "client_secret": settings.keycloak_client_secret,
        "refresh_token": refresh_token,
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(settings.keycloak_token_url, data=data)

    if resp.status_code != 200:
        raise UnauthorizedError("Invalid or expired refresh token")

    return resp.json()


async def logout(refresh_token: str) -> None:
    logout_url = f"{settings.keycloak_issuer}/protocol/openid-connect/logout"
    data = {
        "client_id": settings.keycloak_client_id,
        "client_secret": settings.keycloak_client_secret,
        "refresh_token": refresh_token,
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(logout_url, data=data)

    if resp.status_code not in (200, 204):
        logger.warning("Keycloak logout returned non-2xx", extra={"ctx_status": resp.status_code})
