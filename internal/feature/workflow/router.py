from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query

from internal.core.deps import CurrentUserDep, DbSession, require_manager
from internal.feature.audit import service as audit_service
from internal.feature.users import service as users_service
from internal.feature.workflow import service
from internal.feature.workflow.schemas import (
    Page,
    StageOut,
    StageRename,
    StageTransitionIn,
    StageTransitionOut,
    WorkflowCreate,
    WorkflowDetailOut,
    WorkflowOut,
)

router = APIRouter(prefix="/workflows", tags=["workflow"])


async def _detail(db: DbSession, workflow) -> WorkflowDetailOut:
    stages = await service.list_stages(db, workflow.id)
    return WorkflowDetailOut(
        **WorkflowOut.model_validate(workflow).model_dump(),
        stages=[StageOut.model_validate(s) for s in stages],
    )


@router.post("", response_model=WorkflowDetailOut, status_code=201, dependencies=[Depends(require_manager)])
async def create_workflow(payload: WorkflowCreate, db: DbSession, user: CurrentUserDep) -> WorkflowDetailOut:
    workflow = await service.create_workflow(db, payload)
    await audit_service.record(
        db, action="create", entity="workflow", entity_id=str(workflow.id),
        user_id=user.id, username=user.username,
    )
    return await _detail(db, workflow)


@router.get("", response_model=Page[WorkflowOut])
async def list_workflows(
    db: DbSession, user: CurrentUserDep,
    university_id: uuid.UUID | None = None, direction_id: uuid.UUID | None = None,
    product_id: uuid.UUID | None = None, status: str | None = None, manager_id: uuid.UUID | None = None,
    limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
) -> Page[WorkflowOut]:
    scope = await users_service.get_accessible_university_ids(db, user)
    items, total = await service.list_workflows(
        db, university_id=university_id, direction_id=direction_id, product_id=product_id,
        status=status, manager_id=manager_id, accessible_university_ids=scope,
        limit=limit, offset=offset,
    )
    return Page(items=[WorkflowOut.model_validate(i) for i in items], total=total, limit=limit, offset=offset)


@router.get("/{workflow_id}", response_model=WorkflowDetailOut)
async def get_workflow(workflow_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> WorkflowDetailOut:
    workflow = await service.get_workflow(db, workflow_id)
    return await _detail(db, workflow)


@router.patch("/{workflow_id}/stages/{stage_id}", response_model=StageOut)
async def transition_stage(
    workflow_id: uuid.UUID, stage_id: uuid.UUID, payload: StageTransitionIn, db: DbSession, user: CurrentUserDep
) -> StageOut:
    stage = await service.transition_stage(
        db, workflow_id=workflow_id, stage_id=stage_id, payload=payload, user_id=user.id
    )
    await audit_service.record(
        db, action="stage_transition", entity="stage", entity_id=str(stage_id),
        user_id=user.id, username=user.username,
        payload={"to_status": payload.to_status, "comment": payload.comment},
    )
    return StageOut.model_validate(stage)


@router.patch(
    "/{workflow_id}/stages/{stage_id}/rename", response_model=StageOut, dependencies=[Depends(require_manager)]
)
async def rename_stage(
    workflow_id: uuid.UUID, stage_id: uuid.UUID, payload: StageRename, db: DbSession, user: CurrentUserDep
) -> StageOut:
    stage = await service.rename_stage(db, workflow_id=workflow_id, stage_id=stage_id, payload=payload)
    await audit_service.record(
        db, action="stage_rename", entity="stage", entity_id=str(stage_id),
        user_id=user.id, username=user.username, payload=payload.model_dump(exclude_unset=True),
    )
    return StageOut.model_validate(stage)


@router.get("/{workflow_id}/stages/{stage_id}/transitions", response_model=list[StageTransitionOut])
async def get_transitions(
    workflow_id: uuid.UUID, stage_id: uuid.UUID, db: DbSession, user: CurrentUserDep
) -> list[StageTransitionOut]:
    items = await service.list_transitions(db, workflow_id=workflow_id, stage_id=stage_id)
    return [StageTransitionOut.model_validate(i) for i in items]
