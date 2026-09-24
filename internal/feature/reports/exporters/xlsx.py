from __future__ import annotations

import io
from typing import Any

import openpyxl

from internal.feature.reports.builder import REPORT_COLUMNS


def build_xlsx(dataset: list[dict[str, Any]]) -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Отчёт"
    ws.append(REPORT_COLUMNS)

    for row in dataset:
        ws.append([row.get(col, "") for col in REPORT_COLUMNS])

    for col_cells in ws.columns:
        width = max((len(str(c.value)) for c in col_cells if c.value is not None), default=10)
        ws.column_dimensions[col_cells[0].column_letter].width = min(width + 2, 60)

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
