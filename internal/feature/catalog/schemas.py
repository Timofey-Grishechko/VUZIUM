from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int


# --- University ---------------------------------------------------------

class UniversityCreate(BaseModel):
    name: str
    region: str | None = None
    status: str = "active"


class UniversityUpdate(BaseModel):
    name: str | None = None
    region: str | None = None
    status: str | None = None


class UniversityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    region: str | None
    status: str
    created_at: datetime


# --- Vendor --------------------------------------------------------------

class VendorCreate(BaseModel):
    name: str


class VendorUpdate(BaseModel):
    name: str | None = None


class VendorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    created_at: datetime


# --- ITDirection -----------------------------------------------------------

class ITDirectionCreate(BaseModel):
    name: str


class ITDirectionUpdate(BaseModel):
    name: str | None = None


class ITDirectionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    created_at: datetime


# --- ITProduct -------------------------------------------------------------

class ITProductCreate(BaseModel):
    vendor_id: uuid.UUID
    direction_id: uuid.UUID | None = None
    name: str
    description: str | None = None


class ITProductUpdate(BaseModel):
    vendor_id: uuid.UUID | None = None
    direction_id: uuid.UUID | None = None
    name: str | None = None
    description: str | None = None


class ITProductOut(BaseModel):
    id: uuid.UUID
    vendor_id: uuid.UUID
    vendor_name: str
    direction_id: uuid.UUID | None
    direction_name: str | None
    name: str
    description: str | None
    created_at: datetime

    @classmethod
    def from_model(cls, obj) -> "ITProductOut":
        return cls(
            id=obj.id,
            vendor_id=obj.vendor_id,
            vendor_name=obj.vendor.name if obj.vendor else "",
            direction_id=obj.direction_id,
            direction_name=obj.direction.name if obj.direction else None,
            name=obj.name,
            description=obj.description,
            created_at=obj.created_at,
        )


# --- Responsible -----------------------------------------------------------

class ResponsibleCreate(BaseModel):
    university_id: uuid.UUID
    fio: str
    email: str | None = None
    phone: str | None = None
    side: str = "university"


class ResponsibleUpdate(BaseModel):
    fio: str | None = None
    email: str | None = None
    phone: str | None = None
    side: str | None = None


class ResponsibleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    university_id: uuid.UUID
    fio: str
    email: str | None
    phone: str | None
    side: str
    created_at: datetime


# --- License -----------------------------------------------------------

class LicenseCreate(BaseModel):
    product_id: uuid.UUID
    university_id: uuid.UUID
    contract_number: str | None = None
    signed_at: date | None = None
    expires_at: date | None = None
    transfer_status: str = "pending"


class LicenseUpdate(BaseModel):
    contract_number: str | None = None
    signed_at: date | None = None
    expires_at: date | None = None
    transfer_status: str | None = None


class LicenseOut(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    university_id: uuid.UUID
    university_name: str
    contract_number: str | None
    signed_at: date | None
    expires_at: date | None
    transfer_status: str
    created_at: datetime

    @classmethod
    def from_model(cls, obj) -> "LicenseOut":
        return cls(
            id=obj.id,
            product_id=obj.product_id,
            product_name=obj.product.name if obj.product else "",
            university_id=obj.university_id,
            university_name=obj.university.name if obj.university else "",
            contract_number=obj.contract_number,
            signed_at=obj.signed_at,
            expires_at=obj.expires_at,
            transfer_status=obj.transfer_status,
            created_at=obj.created_at,
        )
