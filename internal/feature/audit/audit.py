"""
Точка входа фичи audit, по аналогии с остальными модулями (catalog.py,
users.py и т.д.). Сама реализация разбита на models/schemas/service/
router/middleware.py — оставлено так для читаемости, т.к. audit
затрагивает сразу и общий middleware, и админский эндпоинт.
"""

from internal.feature.audit.router import router

__all__ = ["router"]
