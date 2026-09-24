"""
Точка входа фичи imports: реэкспорт router. Пайплайн: upload xlsx ->
mapping колонок на поля из ТЗ -> run (валидация построчно + заглушка
персиста, см. service.py::_persist_row).
"""

from internal.feature.imports.router import router

__all__ = ["router"]
