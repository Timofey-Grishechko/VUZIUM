from __future__ import annotations

import io
import uuid
from datetime import timedelta

import anyio
from minio import Minio

from internal.core.config import settings
from internal.core.logger import get_logger

logger = get_logger(__name__)

_client = Minio(
    settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure,
)


async def ensure_bucket() -> None:
    """Создаёт бакет, если его ещё нет. Вызвать один раз при старте приложения."""

    def _ensure() -> None:
        if not _client.bucket_exists(settings.minio_bucket):
            _client.make_bucket(settings.minio_bucket)
            logger.info("MinIO bucket created", extra={"ctx_bucket": settings.minio_bucket})

    await anyio.to_thread.run_sync(_ensure)


def build_object_key(filename: str) -> str:
    """Генерирует уникальный ключ объекта, сохраняя расширение исходного файла."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex


async def upload_bytes(key: str, data: bytes, content_type: str) -> None:
    def _put() -> None:
        _client.put_object(
            settings.minio_bucket,
            key,
            io.BytesIO(data),
            length=len(data),
            content_type=content_type,
        )

    await anyio.to_thread.run_sync(_put)


async def download_bytes(key: str) -> bytes:
    def _get() -> bytes:
        response = _client.get_object(settings.minio_bucket, key)
        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()

    return await anyio.to_thread.run_sync(_get)


async def presigned_get_url(key: str) -> str:
    def _url() -> str:
        return _client.presigned_get_object(
            settings.minio_bucket,
            key,
            expires=timedelta(seconds=settings.minio_presigned_ttl_sec),
        )

    return await anyio.to_thread.run_sync(_url)


async def delete_object(key: str) -> None:
    def _delete() -> None:
        _client.remove_object(settings.minio_bucket, key)

    await anyio.to_thread.run_sync(_delete)
