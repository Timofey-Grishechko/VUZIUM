"""
Точка входа фичи catalog: реэкспорт router. Модели/схемы/generic CRUD
разбиты по файлам (models.py, crud.py, schemas.py, service.py,
router.py) — 6 справочных сущностей из ТЗ: University, Vendor,
ITDirection, ITProduct, Responsible, License.
"""

from internal.feature.catalog.router import router

__all__ = ["router"]
