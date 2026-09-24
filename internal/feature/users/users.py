"""
Точка входа фичи users: реэкспорт router. Локальный User upsert'ится
из проверенного JWT (get_or_create_from_token) — используется также
из catalog/workflow для получения users.id и для AccessScope-фильтрации.
"""

from internal.feature.users.router import router

__all__ = ["router"]
