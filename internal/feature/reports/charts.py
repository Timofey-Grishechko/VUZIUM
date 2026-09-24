from __future__ import annotations

import io
from collections import Counter
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def status_distribution_png(dataset: list[dict[str, Any]]) -> bytes:
    """Столбчатая диаграмма количества записей по статусам, PNG-байты."""
    counts = Counter(row.get("status", "—") for row in dataset)

    fig, ax = plt.subplots(figsize=(6, 4))
    if counts:
        ax.bar(list(counts.keys()), list(counts.values()))
        ax.set_ylabel("Количество")
        ax.set_title("Распределение по статусам")
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    else:
        ax.text(0.5, 0.5, "Нет данных", ha="center", va="center")
        ax.axis("off")

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    return buf.getvalue()
