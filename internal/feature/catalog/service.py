from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from internal.feature.catalog import crud
from internal.feature.catalog.models import ITDirection, ITProduct, License, Responsible, University, Vendor
from internal.feature.catalog.schemas import (
    ITDirectionCreate,
    ITDirectionUpdate,
    ITProductCreate,
    ITProductUpdate,
    LicenseCreate,
    LicenseUpdate,
    ResponsibleCreate,
    ResponsibleUpdate,
    UniversityCreate,
    UniversityUpdate,
    VendorCreate,
    VendorUpdate,
)

# --- University --------------------------------------------------------

async def list_universities(session: AsyncSession, *, name: str | None, status: str | None, limit: int, offset: int):
    return await crud.list_paginated(
        session, University, filters={"name": name, "status": status}, limit=limit, offset=offset,
        order_by=University.name,
    )


async def get_university(session: AsyncSession, obj_id: UUID) -> University:
    return await crud.get_or_404(session, University, obj_id, "University not found")


async def create_university(session: AsyncSession, payload: UniversityCreate) -> University:
    return await crud.create_obj(session, University, **payload.model_dump())


async def update_university(session: AsyncSession, obj_id: UUID, payload: UniversityUpdate) -> University:
    obj = await get_university(session, obj_id)
    return await crud.update_obj(session, obj, **payload.model_dump(exclude_unset=True))


async def delete_university(session: AsyncSession, obj_id: UUID) -> None:
    obj = await get_university(session, obj_id)
    await crud.delete_obj(session, obj)


# --- Vendor --------------------------------------------------------

async def list_vendors(session: AsyncSession, *, name: str | None, limit: int, offset: int):
    return await crud.list_paginated(
        session, Vendor, filters={"name": name}, limit=limit, offset=offset, order_by=Vendor.name
    )


async def get_vendor(session: AsyncSession, obj_id: UUID) -> Vendor:
    return await crud.get_or_404(session, Vendor, obj_id, "Vendor not found")


async def create_vendor(session: AsyncSession, payload: VendorCreate) -> Vendor:
    return await crud.create_obj(session, Vendor, **payload.model_dump())


async def update_vendor(session: AsyncSession, obj_id: UUID, payload: VendorUpdate) -> Vendor:
    obj = await get_vendor(session, obj_id)
    return await crud.update_obj(session, obj, **payload.model_dump(exclude_unset=True))


async def delete_vendor(session: AsyncSession, obj_id: UUID) -> None:
    obj = await get_vendor(session, obj_id)
    await crud.delete_obj(session, obj)


# --- ITDirection --------------------------------------------------------

async def list_directions(session: AsyncSession, *, name: str | None, limit: int, offset: int):
    return await crud.list_paginated(
        session, ITDirection, filters={"name": name}, limit=limit, offset=offset, order_by=ITDirection.name
    )


async def get_direction(session: AsyncSession, obj_id: UUID) -> ITDirection:
    return await crud.get_or_404(session, ITDirection, obj_id, "IT direction not found")


async def create_direction(session: AsyncSession, payload: ITDirectionCreate) -> ITDirection:
    return await crud.create_obj(session, ITDirection, **payload.model_dump())


async def update_direction(session: AsyncSession, obj_id: UUID, payload: ITDirectionUpdate) -> ITDirection:
    obj = await get_direction(session, obj_id)
    return await crud.update_obj(session, obj, **payload.model_dump(exclude_unset=True))


async def delete_direction(session: AsyncSession, obj_id: UUID) -> None:
    obj = await get_direction(session, obj_id)
    await crud.delete_obj(session, obj)


# --- ITProduct --------------------------------------------------------

async def list_products(
    session: AsyncSession, *, name: str | None, vendor_id: UUID | None, direction_id: UUID | None,
    limit: int, offset: int,
):
    return await crud.list_paginated(
        session, ITProduct,
        filters={"name": name, "vendor_id": vendor_id, "direction_id": direction_id},
        limit=limit, offset=offset, order_by=ITProduct.name,
    )


async def get_product(session: AsyncSession, obj_id: UUID) -> ITProduct:
    return await crud.get_or_404(session, ITProduct, obj_id, "IT product not found")


async def create_product(session: AsyncSession, payload: ITProductCreate) -> ITProduct:
    await get_vendor(session, payload.vendor_id)  # проверяем, что вендор существует
    if payload.direction_id is not None:
        await get_direction(session, payload.direction_id)
    return await crud.create_obj(session, ITProduct, **payload.model_dump())


async def update_product(session: AsyncSession, obj_id: UUID, payload: ITProductUpdate) -> ITProduct:
    obj = await get_product(session, obj_id)
    if payload.vendor_id is not None:
        await get_vendor(session, payload.vendor_id)
    if payload.direction_id is not None:
        await get_direction(session, payload.direction_id)
    return await crud.update_obj(session, obj, **payload.model_dump(exclude_unset=True))


async def delete_product(session: AsyncSession, obj_id: UUID) -> None:
    obj = await get_product(session, obj_id)
    await crud.delete_obj(session, obj)


# --- Responsible --------------------------------------------------------

async def list_responsibles(session: AsyncSession, *, university_id: UUID | None, fio: str | None, limit: int, offset: int):
    return await crud.list_paginated(
        session, Responsible, filters={"university_id": university_id, "fio": fio},
        limit=limit, offset=offset, order_by=Responsible.fio,
    )


async def get_responsible(session: AsyncSession, obj_id: UUID) -> Responsible:
    return await crud.get_or_404(session, Responsible, obj_id, "Responsible not found")


async def create_responsible(session: AsyncSession, payload: ResponsibleCreate) -> Responsible:
    await get_university(session, payload.university_id)
    return await crud.create_obj(session, Responsible, **payload.model_dump())


async def update_responsible(session: AsyncSession, obj_id: UUID, payload: ResponsibleUpdate) -> Responsible:
    obj = await get_responsible(session, obj_id)
    return await crud.update_obj(session, obj, **payload.model_dump(exclude_unset=True))


async def delete_responsible(session: AsyncSession, obj_id: UUID) -> None:
    obj = await get_responsible(session, obj_id)
    await crud.delete_obj(session, obj)


# --- License --------------------------------------------------------

async def list_licenses(
    session: AsyncSession, *, university_id: UUID | None, product_id: UUID | None,
    transfer_status: str | None, limit: int, offset: int,
    accessible_university_ids: list[UUID] | None = None,
):
    filters: dict = {"university_id": university_id, "product_id": product_id, "transfer_status": transfer_status}
    items, total = await crud.list_paginated(session, License, filters=filters, limit=limit, offset=offset)

    if accessible_university_ids is not None:
        allowed = set(accessible_university_ids)
        items = [i for i in items if i.university_id in allowed]
        total = len(items)  # приближённо: точная фильтрация по scope на уровне SQL — TODO при росте объёма данных

    return items, total


async def get_license(session: AsyncSession, obj_id: UUID) -> License:
    return await crud.get_or_404(session, License, obj_id, "License not found")


async def create_license(session: AsyncSession, payload: LicenseCreate) -> License:
    await get_product(session, payload.product_id)
    await get_university(session, payload.university_id)
    return await crud.create_obj(session, License, **payload.model_dump())


async def update_license(session: AsyncSession, obj_id: UUID, payload: LicenseUpdate) -> License:
    obj = await get_license(session, obj_id)
    return await crud.update_obj(session, obj, **payload.model_dump(exclude_unset=True))


async def delete_license(session: AsyncSession, obj_id: UUID) -> None:
    obj = await get_license(session, obj_id)
    await crud.delete_obj(session, obj)
