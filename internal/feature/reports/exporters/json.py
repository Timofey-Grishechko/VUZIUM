from __future__ import annotations

import json
from typing import Any


def build_json(dataset: list[dict[str, Any]]) -> bytes:
    return json.dumps(dataset, ensure_ascii=False, indent=2).encode("utf-8")
