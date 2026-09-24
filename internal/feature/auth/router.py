from __future__ import annotations

from fastapi import APIRouter

from internal.core.deps import CurrentUserDep
from internal.feature.auth import service
from internal.feature.auth.schemas import LoginRequest, MeResponse, RefreshRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    token_data = await service.login(payload.username, payload.password)
    return TokenResponse(**token_data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest) -> TokenResponse:
    token_data = await service.refresh(payload.refresh_token)
    return TokenResponse(**token_data)


@router.post("/logout", status_code=204)
async def logout(payload: RefreshRequest) -> None:
    await service.logout(payload.refresh_token)


@router.get("/me", response_model=MeResponse)
async def me(user: CurrentUserDep) -> MeResponse:
    return MeResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        roles=user.roles,
        is_admin=user.is_admin,
        is_manager=user.is_manager,
    )
