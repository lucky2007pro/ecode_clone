"""
school-service Pydantic sxemalari.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


# --- TARIFF PLAN SCHEMAS ---
class TariffPlanBase(BaseModel):
    name: str
    price: float
    max_students: int
    max_courses: int
    max_storage_gb: int = 10


class TariffPlanCreate(TariffPlanBase):
    pass


class TariffPlanResponse(TariffPlanBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


# --- SCHOOL SCHEMAS ---
class SchoolBase(BaseModel):
    name: str
    subdomain: str
    custom_domain: str | None = None
    logo_url: str | None = None
    settings: dict = {}


class SchoolCreate(SchoolBase):
    owner_id: uuid.UUID
    tariff_plan_id: uuid.UUID


class SchoolUpdate(BaseModel):
    name: str | None = None
    custom_domain: str | None = None
    logo_url: str | None = None
    settings: dict | None = None
    tariff_plan_id: uuid.UUID | None = None
    is_active: bool | None = None


class SchoolResponse(SchoolBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    owner_id: uuid.UUID
    tariff_plan_id: uuid.UUID
    is_active: bool
    created_at: datetime
