"""
Точка входа фичи files: реэкспорт router (см. models.py/service.py/
storage.py/router.py — разбито на файлы для читаемости, MinIO-клиент
переиспользуется модулями imports и reports).
"""

from internal.feature.files.router import router

__all__ = ["router"]
