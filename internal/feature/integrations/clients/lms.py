from __future__ import annotations

from typing import Any

import httpx


class LMSClient:
    """
    httpx-клиент интеграции с LMS. base_url/api_key берутся из
    конкретного IntegrationSource (их может быть несколько), а не из
    глобальных settings.
    """

    def __init__(self, base_url: str, api_key: str | None = None, timeout: float = 15.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self._timeout = timeout

    async def fetch_enrollments(self) -> list[dict[str, Any]]:
        """
        Список зачислений/курсов из LMS. Точный путь и формат ответа
        уточнить с реальным API LMS — пока используется правдоподобный
        эндпоинт `/api/enrollments`, поправить при интеграции.
        """
        async with httpx.AsyncClient(timeout=self._timeout, headers=self._headers) as client:
            resp = await client.get(f"{self._base_url}/api/enrollments")
            resp.raise_for_status()
            return resp.json()
