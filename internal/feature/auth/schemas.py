from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Keycloak возвращает больше полей, чем нам нужно

    access_token: str
    refresh_token: str | None = None
    expires_in: int
    refresh_expires_in: int | None = None
    token_type: str = "Bearer"


class MeResponse(BaseModel):
    id: str
    username: str
    email: str | None
    roles: list[str]
    is_admin: bool
    is_manager: bool
