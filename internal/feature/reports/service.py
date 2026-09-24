from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from internal.core.errors import NotFoundError, ValidationError
from internal.core.logger import get_logger
from internal.feature.files import storage
from internal.feature.reports import builder
from internal.feature.reports.exporters import json as json_exporter
from internal.feature.reports.exporters import pdf as pdf_exporter
from internal.feature.reports.exporters import xlsx as xlsx_exporter
from internal.feature.reports.models import Report
from internal.feature.reports.schemas import ReportFilters

logger = get_logger(__name__)

_CONTENT_TYPES = {
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "pdf": "application/pdf",
    "json": "application/json",
}


def _export(fmt: str, dataset: list[dict]) -> bytes:
    if fmt == "xlsx":
        return xlsx_exporter.build_xlsx(dataset)
    if fmt == "pdf":
        return pdf_exporter.build_pdf(dataset)
    if fmt == "json":
        return json_exporter.build_json(dataset)
    raise ValidationError(f"Unsupported format: {fmt}")


async def create_report(
    session: AsyncSession, *, fmt: str, filters: ReportFilters, created_by: str | None
) -> Report:
    if fmt not in _CONTENT_TYPES:
        raise ValidationError(f"Unsupported format: {fmt}")

    report = Report(
        type="workflow_summary",
        format=fmt,
        filters=filters.model_dump(mode="json"),
        status="pending",
        created_by=created_by,
    )
    session.add(report)
    await session.commit()
    await session.refresh(report)
    return report


async def get_report(session: AsyncSession, report_id: UUID) -> Report:
    obj = await session.get(Report, report_id)
    if obj is None:
        raise NotFoundError("Report not found")
    return obj


async def run_report_generation(session: AsyncSession, *, report_id: str) -> None:
    """
    Полный пайплайн генерации отчёта. Вызывается из Celery-таска
    (reports/report.py: generate_report_task), не напрямую из HTTP —
    поэтому создание отчёта (POST /reports) не блокирует API.
    """
    report = await get_report(session, UUID(report_id))
    report.status = "processing"
    await session.commit()

    try:
        filters = ReportFilters.model_validate(report.filters)
        dataset = await builder.build_dataset(
            session,
            date_from=filters.date_from,
            date_to=filters.date_to,
            university_id=filters.university_id,
            direction_id=filters.direction_id,
            product_id=filters.product_id,
            responsible_id=filters.responsible_id,
            status=filters.status,
        )

        content = _export(report.format, dataset)
        key = storage.build_object_key(f"report-{report.id}.{report.format}")
        await storage.upload_bytes(key, content, _CONTENT_TYPES[report.format])

        report.file_key = key
        report.status = "done"
        report.finished_at = datetime.now(timezone.utc)
    except Exception as exc:  # noqa: BLE001 — статус отчёта важнее конкретного типа ошибки
        logger.exception("Report generation failed", extra={"ctx_report_id": report_id})
        report.status = "failed"
        report.error = str(exc)[:1000]
        report.finished_at = datetime.now(timezone.utc)

    await session.commit()


async def get_download_url(report: Report) -> str | None:
    if report.status != "done" or not report.file_key:
        return None
    return await storage.presigned_get_url(report.file_key)
