from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from internal.core.errors import NotFoundError, ValidationError
from internal.core.logger import get_logger
from internal.feature.catalog.models import ITDirection, ITProduct, University
from internal.feature.workflow.models import Stage, StageTransition, Workflow
from internal.feature.workflow.schemas import StageRename, StageTransitionIn, WorkflowCreate

logger = get_logger(__name__)

# 14 этапов по умолчанию (см. ТЗ). Названия/порядок редактируются после
# создания через PATCH /workflows/{id}/stages/{stage_id}/rename.
DEFAULT_STAGES: list[str] = [
    "Первичный контакт",
    "Коммерческое предложение направлено",
    "Согласование условий",
    "Договор подготовлен",
    "Договор подписан",
    "Счёт выставлен",
    "Оплата получена",
    "Лицензия передана",
    "Настройка/внедрение",
    "Обучение пользователей",
    "Приёмка ВУЗом",
    "Сбор обратной связи",
    "Продление/апсейл",
    "Закрытие сделки",
]


async def create_workflow(session: AsyncSession, payload: WorkflowCreate) -> Workflow:
    if await session.get(University, payload.university_id) is None:
        raise ValidationError("University not found")
    if payload.direction_id is not None and await session.get(ITDirection, payload.direction_id) is None:
        raise ValidationError("IT direction not found")
    if payload.product_id is not None and await session.get(ITProduct, payload.product_id) is None:
        raise ValidationError("IT product not found")

    workflow = Workflow(
        university_id=payload.university_id,
        direction_id=payload.direction_id,
        product_id=payload.product_id,
        manager_id=payload.manager_id,
    )
    session.add(workflow)
    await session.flush()  # получаем workflow.id для этапов, ещё без коммита

    for i, name in enumerate(DEFAULT_STAGES, start=1):
        session.add(Stage(workflow_id=workflow.id, order=i, name=name, status="pending"))

    await session.commit()
    await session.refresh(workflow)
    return workflow


async def list_workflows(
    session: AsyncSession,
    *,
    university_id: UUID | None,
    direction_id: UUID | None,
    product_id: UUID | None,
    status: str | None,
    manager_id: UUID | None,
    accessible_university_ids: list[UUID] | None,
    limit: int,
    offset: int,
) -> tuple[list[Workflow], int]:
    query = select(Workflow)
    count_query = select(func.count()).select_from(Workflow)

    conditions = []
    if university_id:
        conditions.append(Workflow.university_id == university_id)
    if direction_id:
        conditions.append(Workflow.direction_id == direction_id)
    if product_id:
        conditions.append(Workflow.product_id == product_id)
    if status:
        conditions.append(Workflow.status == status)
    if manager_id:
        conditions.append(Workflow.manager_id == manager_id)
    if accessible_university_ids is not None:
        conditions.append(Workflow.university_id.in_(accessible_university_ids))

    for cond in conditions:
        query = query.where(cond)
        count_query = count_query.where(cond)

    query = query.order_by(Workflow.created_at.desc()).limit(limit).offset(offset)

    items = (await session.execute(query)).scalars().all()
    total = (await session.execute(count_query)).scalar_one()
    return list(items), total


async def get_workflow(session: AsyncSession, workflow_id: UUID) -> Workflow:
    obj = await session.get(Workflow, workflow_id)
    if obj is None:
        raise NotFoundError("Workflow not found")
    return obj


async def list_stages(session: AsyncSession, workflow_id: UUID) -> list[Stage]:
    result = await session.execute(
        select(Stage).where(Stage.workflow_id == workflow_id).order_by(Stage.order)
    )
    return list(result.scalars().all())


async def get_stage(session: AsyncSession, workflow_id: UUID, stage_id: UUID) -> Stage:
    stage = await session.get(Stage, stage_id)
    if stage is None or stage.workflow_id != workflow_id:
        raise NotFoundError("Stage not found")
    return stage


async def transition_stage(
    session: AsyncSession, *, workflow_id: UUID, stage_id: UUID, payload: StageTransitionIn, user_id: str
) -> Stage:
    stage = await get_stage(session, workflow_id, stage_id)
    from_status = stage.status
    stage.status = payload.to_status
    if payload.comment is not None:
        stage.comment = payload.comment

    session.add(
        StageTransition(
            stage_id=stage.id,
            from_status=from_status,
            to_status=payload.to_status,
            user_id=user_id,
            comment=payload.comment,
        )
    )

    # Если это был последний этап и он закрыт — считаем весь workflow завершённым.
    stages = await list_stages(session, workflow_id)
    if all(s.status == "done" for s in stages if s.id != stage.id) and payload.to_status == "done":
        workflow = await get_workflow(session, workflow_id)
        workflow.status = "done"

    await session.commit()
    await session.refresh(stage)
    return stage


async def rename_stage(session: AsyncSession, *, workflow_id: UUID, stage_id: UUID, payload: StageRename) -> Stage:
    stage = await get_stage(session, workflow_id, stage_id)
    if payload.name is not None:
        stage.name = payload.name
    if payload.order is not None:
        stage.order = payload.order
    await session.commit()
    await session.refresh(stage)
    return stage


async def list_transitions(session: AsyncSession, *, workflow_id: UUID, stage_id: UUID) -> list[StageTransition]:
    await get_stage(session, workflow_id, stage_id)  # проверяем, что этап принадлежит этому workflow
    result = await session.execute(
        select(StageTransition)
        .where(StageTransition.stage_id == stage_id)
        .order_by(StageTransition.created_at.desc())
    )
    return list(result.scalars().all())
