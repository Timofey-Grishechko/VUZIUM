"""
Точка входа фичи auth: /auth/login, /auth/refresh, /auth/logout —
прокси до Keycloak token endpoint (Resource Owner Password grant,
клиенту не нужен keycloak-js), /auth/me — текущий пользователь из
уже проверенного JWT (см. core/security.py, не трогаю). Требует
включённого "Direct Access Grants" на клиенте в Keycloak.
"""

from internal.feature.auth.router import router

__all__ = ["router"]
