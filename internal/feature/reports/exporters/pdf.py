from __future__ import annotations

import io
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from internal.feature.reports.builder import REPORT_COLUMNS
from internal.feature.reports.charts import status_distribution_png


def build_pdf(dataset: list[dict[str, Any]], *, title: str = "Отчёт") -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=landscape(A4), leftMargin=1.5 * cm, rightMargin=1.5 * cm
    )
    styles = getSampleStyleSheet()

    elements = [Paragraph(title, styles["Title"]), Spacer(1, 0.5 * cm)]

    chart_png = status_distribution_png(dataset)
    elements.append(Image(io.BytesIO(chart_png), width=14 * cm, height=9 * cm))
    elements.append(Spacer(1, 0.5 * cm))

    table_data = [REPORT_COLUMNS] + [
        [str(row.get(col, "")) for col in REPORT_COLUMNS] for row in dataset
    ]
    table = Table(table_data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f6f7")]),
            ]
        )
    )
    elements.append(table)

    doc.build(elements)
    return buf.getvalue()
