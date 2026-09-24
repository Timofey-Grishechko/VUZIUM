from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends

from internal.core.deps import CurrentUserDep, DbSession, require_manager
from internal.feature.reports import service
from internal.feature.reports.schemas import ReportCreate, ReportStatusOut

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("", response_model=ReportStatusOut, status_code=202, dependencies=[Depends(require_manager)])
async def create_report(payload: ReportCreate, db: DbSession, user: CurrentUserDep) -> ReportStatusOut:
    report = await service.create_report(
        db, fmt=payload.format, filters=payload.filters, created_by=user.id
    )

    # Локальный импорт — report.py реэкспортирует этот router,
    # импорт на уровне модуля создал бы цикл.
    from internal.feature.reports.report import generate_report_task

    generate_report_task.delay(str(report.id))

    return ReportStatusOut.model_validate(report)


@router.get("/{report_id}", response_model=ReportStatusOut)
async def get_report_status(report_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> ReportStatusOut:
    report = await service.get_report(db, report_id)
    url = await service.get_download_url(report)
    data = ReportStatusOut.model_validate(report).model_dump()
    data["download_url"] = url
    return ReportStatusOut(**data)
