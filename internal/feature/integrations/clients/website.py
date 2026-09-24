from __future__ import annotations

from typing import Any

import httpx


class WebsiteClient:
    """httpx-клиент интеграции с сайтом (заявки/заказы на ПО)."""

    def __init__(self, base_url: str, api_key: str | None = None, timeout: float = 15.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self._timeout = timeout

    async def fetch_orders(self) -> list[dict[str, Any]]:
        """
        Список заявок с сайта. Путь `/api/orders` — правдоподобная
        заглушка, поправить под реальный API сайта при интеграции.
        """
        async with httpx.AsyncClient(timeout=self._timeout, headers=self._headers) as client:
            resp = await client.get(f"{self._base_url}/api/orders")
            resp.raise_for_status()
            return resp.json()
