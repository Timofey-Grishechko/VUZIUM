from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query

from internal.core.deps import CurrentUserDep, DbSession, require_admin, require_manager
from internal.feature.audit import service as audit_service
from internal.feature.catalog import service
from internal.feature.catalog.schemas import (
    ITDirectionCreate,
    ITDirectionOut,
    ITDirectionUpdate,
    ITProductCreate,
    ITProductOut,
    ITProductUpdate,
    LicenseCreate,
    LicenseOut,
    LicenseUpdate,
    Page,
    ResponsibleCreate,
    ResponsibleOut,
    ResponsibleUpdate,
    UniversityCreate,
    UniversityOut,
    UniversityUpdate,
    VendorCreate,
    VendorOut,
    VendorUpdate,
)
from internal.feature.users import service as users_service

router = APIRouter(prefix="/catalog", tags=["catalog"])


async def _audit(db: DbSession, user, *, action: str, entity: str, entity_id: str, payload: dict | None = None) -> None:
    await audit_service.record(
        db, action=action, entity=entity, entity_id=entity_id, user_id=user.id, username=user.username, payload=payload
    )


# --- University --------------------------------------------------------

@router.get("/universities", response_model=Page[UniversityOut])
async def list_universities(
    db: DbSession, user: CurrentUserDep,
    name: str | None = None, status: str | None = None,
    limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
) -> Page[UniversityOut]:
    items, total = await service.list_universities(db, name=name, status=status, limit=limit, offset=offset)
    return Page(items=[UniversityOut.model_validate(i) for i in items], total=total, limit=limit, offset=offset)


@router.post("/universities", response_model=UniversityOut, status_code=201, dependencies=[Depends(require_manager)])
async def create_university(payload: UniversityCreate, db: DbSession, user: CurrentUserDep) -> UniversityOut:
    obj = await service.create_university(db, payload)
    await _audit(db, user, action="create", entity="university", entity_id=str(obj.id))
    return UniversityOut.model_validate(obj)


@router.get("/universities/{obj_id}", response_model=UniversityOut)
async def get_university(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> UniversityOut:
    return UniversityOut.model_validate(await service.get_university(db, obj_id))


@router.patch("/universities/{obj_id}", response_model=UniversityOut, dependencies=[Depends(require_manager)])
async def update_university(obj_id: uuid.UUID, payload: UniversityUpdate, db: DbSession, user: CurrentUserDep) -> UniversityOut:
    obj = await service.update_university(db, obj_id, payload)
    await _audit(db, user, action="update", entity="university", entity_id=str(obj_id))
    return UniversityOut.model_validate(obj)


@router.delete("/universities/{obj_id}", status_code=204, dependencies=[Depends(require_admin)])
async def delete_university(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> None:
    await service.delete_university(db, obj_id)
    await _audit(db, user, action="delete", entity="university", entity_id=str(obj_id))


# --- Vendor --------------------------------------------------------

@router.get("/vendors", response_model=Page[VendorOut])
async def list_vendors(
    db: DbSession, user: CurrentUserDep, name: str | None = None,
    limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
) -> Page[VendorOut]:
    items, total = await service.list_vendors(db, name=name, limit=limit, offset=offset)
    return Page(items=[VendorOut.model_validate(i) for i in items], total=total, limit=limit, offset=offset)


@router.post("/vendors", response_model=VendorOut, status_code=201, dependencies=[Depends(require_manager)])
async def create_vendor(payload: VendorCreate, db: DbSession, user: CurrentUserDep) -> VendorOut:
    obj = await service.create_vendor(db, payload)
    await _audit(db, user, action="create", entity="vendor", entity_id=str(obj.id))
    return VendorOut.model_validate(obj)


@router.get("/vendors/{obj_id}", response_model=VendorOut)
async def get_vendor(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> VendorOut:
    return VendorOut.model_validate(await service.get_vendor(db, obj_id))


@router.patch("/vendors/{obj_id}", response_model=VendorOut, dependencies=[Depends(require_manager)])
async def update_vendor(obj_id: uuid.UUID, payload: VendorUpdate, db: DbSession, user: CurrentUserDep) -> VendorOut:
    obj = await service.update_vendor(db, obj_id, payload)
    await _audit(db, user, action="update", entity="vendor", entity_id=str(obj_id))
    return VendorOut.model_validate(obj)


@router.delete("/vendors/{obj_id}", status_code=204, dependencies=[Depends(require_admin)])
async def delete_vendor(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> None:
    await service.delete_vendor(db, obj_id)
    await _audit(db, user, action="delete", entity="vendor", entity_id=str(obj_id))


# --- ITDirection --------------------------------------------------------

@router.get("/directions", response_model=Page[ITDirectionOut])
async def list_directions(
    db: DbSession, user: CurrentUserDep, name: str | None = None,
    limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
) -> Page[ITDirectionOut]:
    items, total = await service.list_directions(db, name=name, limit=limit, offset=offset)
    return Page(items=[ITDirectionOut.model_validate(i) for i in items], total=total, limit=limit, offset=offset)


@router.post("/directions", response_model=ITDirectionOut, status_code=201, dependencies=[Depends(require_manager)])
async def create_direction(payload: ITDirectionCreate, db: DbSession, user: CurrentUserDep) -> ITDirectionOut:
    obj = await service.create_direction(db, payload)
    await _audit(db, user, action="create", entity="it_direction", entity_id=str(obj.id))
    return ITDirectionOut.model_validate(obj)


@router.get("/directions/{obj_id}", response_model=ITDirectionOut)
async def get_direction(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> ITDirectionOut:
    return ITDirectionOut.model_validate(await service.get_direction(db, obj_id))


@router.patch("/directions/{obj_id}", response_model=ITDirectionOut, dependencies=[Depends(require_manager)])
async def update_direction(obj_id: uuid.UUID, payload: ITDirectionUpdate, db: DbSession, user: CurrentUserDep) -> ITDirectionOut:
    obj = await service.update_direction(db, obj_id, payload)
    await _audit(db, user, action="update", entity="it_direction", entity_id=str(obj_id))
    return ITDirectionOut.model_validate(obj)


@router.delete("/directions/{obj_id}", status_code=204, dependencies=[Depends(require_admin)])
async def delete_direction(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> None:
    await service.delete_direction(db, obj_id)
    await _audit(db, user, action="delete", entity="it_direction", entity_id=str(obj_id))


# --- ITProduct --------------------------------------------------------

@router.get("/products", response_model=Page[ITProductOut])
async def list_products(
    db: DbSession, user: CurrentUserDep,
    name: str | None = None, vendor_id: uuid.UUID | None = None, direction_id: uuid.UUID | None = None,
    limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
) -> Page[ITProductOut]:
    items, total = await service.list_products(
        db, name=name, vendor_id=vendor_id, direction_id=direction_id, limit=limit, offset=offset
    )
    return Page(items=[ITProductOut.from_model(i) for i in items], total=total, limit=limit, offset=offset)


@router.post("/products", response_model=ITProductOut, status_code=201, dependencies=[Depends(require_manager)])
async def create_product(payload: ITProductCreate, db: DbSession, user: CurrentUserDep) -> ITProductOut:
    obj = await service.create_product(db, payload)
    await _audit(db, user, action="create", entity="it_product", entity_id=str(obj.id))
    return ITProductOut.from_model(obj)


@router.get("/products/{obj_id}", response_model=ITProductOut)
async def get_product(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> ITProductOut:
    return ITProductOut.from_model(await service.get_product(db, obj_id))


@router.patch("/products/{obj_id}", response_model=ITProductOut, dependencies=[Depends(require_manager)])
async def update_product(obj_id: uuid.UUID, payload: ITProductUpdate, db: DbSession, user: CurrentUserDep) -> ITProductOut:
    obj = await service.update_product(db, obj_id, payload)
    await _audit(db, user, action="update", entity="it_product", entity_id=str(obj_id))
    return ITProductOut.from_model(obj)


@router.delete("/products/{obj_id}", status_code=204, dependencies=[Depends(require_admin)])
async def delete_product(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> None:
    await service.delete_product(db, obj_id)
    await _audit(db, user, action="delete", entity="it_product", entity_id=str(obj_id))


# --- Responsible --------------------------------------------------------

@router.get("/responsibles", response_model=Page[ResponsibleOut])
async def list_responsibles(
    db: DbSession, user: CurrentUserDep,
    university_id: uuid.UUID | None = None, fio: str | None = None,
    limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
) -> Page[ResponsibleOut]:
    items, total = await service.list_responsibles(db, university_id=university_id, fio=fio, limit=limit, offset=offset)
    return Page(items=[ResponsibleOut.model_validate(i) for i in items], total=total, limit=limit, offset=offset)


@router.post("/responsibles", response_model=ResponsibleOut, status_code=201, dependencies=[Depends(require_manager)])
async def create_responsible(payload: ResponsibleCreate, db: DbSession, user: CurrentUserDep) -> ResponsibleOut:
    obj = await service.create_responsible(db, payload)
    await _audit(db, user, action="create", entity="responsible", entity_id=str(obj.id))
    return ResponsibleOut.model_validate(obj)


@router.get("/responsibles/{obj_id}", response_model=ResponsibleOut)
async def get_responsible(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> ResponsibleOut:
    return ResponsibleOut.model_validate(await service.get_responsible(db, obj_id))


@router.patch("/responsibles/{obj_id}", response_model=ResponsibleOut, dependencies=[Depends(require_manager)])
async def update_responsible(obj_id: uuid.UUID, payload: ResponsibleUpdate, db: DbSession, user: CurrentUserDep) -> ResponsibleOut:
    obj = await service.update_responsible(db, obj_id, payload)
    await _audit(db, user, action="update", entity="responsible", entity_id=str(obj_id))
    return ResponsibleOut.model_validate(obj)


@router.delete("/responsibles/{obj_id}", status_code=204, dependencies=[Depends(require_manager)])
async def delete_responsible(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> None:
    await service.delete_responsible(db, obj_id)
    await _audit(db, user, action="delete", entity="responsible", entity_id=str(obj_id))


# --- License --------------------------------------------------------

@router.get("/licenses", response_model=Page[LicenseOut])
async def list_licenses(
    db: DbSession, user: CurrentUserDep,
    university_id: uuid.UUID | None = None, product_id: uuid.UUID | None = None,
    transfer_status: str | None = None,
    limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
) -> Page[LicenseOut]:
    scope = await users_service.get_accessible_university_ids(db, user)
    items, total = await service.list_licenses(
        db, university_id=university_id, product_id=product_id, transfer_status=transfer_status,
        limit=limit, offset=offset, accessible_university_ids=scope,
    )
    return Page(items=[LicenseOut.from_model(i) for i in items], total=total, limit=limit, offset=offset)


@router.post("/licenses", response_model=LicenseOut, status_code=201, dependencies=[Depends(require_manager)])
async def create_license(payload: LicenseCreate, db: DbSession, user: CurrentUserDep) -> LicenseOut:
    obj = await service.create_license(db, payload)
    await _audit(db, user, action="create", entity="license", entity_id=str(obj.id))
    return LicenseOut.from_model(obj)


@router.get("/licenses/{obj_id}", response_model=LicenseOut)
async def get_license(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> LicenseOut:
    return LicenseOut.from_model(await service.get_license(db, obj_id))


@router.patch("/licenses/{obj_id}", response_model=LicenseOut, dependencies=[Depends(require_manager)])
async def update_license(obj_id: uuid.UUID, payload: LicenseUpdate, db: DbSession, user: CurrentUserDep) -> LicenseOut:
    obj = await service.update_license(db, obj_id, payload)
    await _audit(db, user, action="update", entity="license", entity_id=str(obj_id))
    return LicenseOut.from_model(obj)


@router.delete("/licenses/{obj_id}", status_code=204, dependencies=[Depends(require_manager)])
async def delete_license(obj_id: uuid.UUID, db: DbSession, user: CurrentUserDep) -> None:
    await service.delete_license(db, obj_id)
    await _audit(db, user, action="delete", entity="license", entity_id=str(obj_id))
