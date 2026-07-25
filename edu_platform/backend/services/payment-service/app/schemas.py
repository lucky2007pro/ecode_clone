"""
payment-service Pydantic sxemalari.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from libs.shared_schemas.enums import PaymentStatus


class PaymentCreate(BaseModel):
    user_id: uuid.UUID
    school_id: uuid.UUID
    course_id: uuid.UUID | None = None
    amount: float
    provider: str  # "payme", "click"


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    school_id: uuid.UUID
    course_id: uuid.UUID | None
    amount: float
    currency: str
    provider: str
    provider_transaction_id: str | None
    status: PaymentStatus
    created_at: datetime


class SubscriptionCreate(BaseModel):
    school_id: uuid.UUID
    tariff_plan_id: uuid.UUID
    duration_days: int = 30


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    school_id: uuid.UUID
    tariff_plan_id: uuid.UUID
    starts_at: datetime
    ends_at: datetime
    is_active: bool
    created_at: datetime
