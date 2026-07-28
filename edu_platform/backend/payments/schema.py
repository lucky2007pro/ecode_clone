import uuid
from datetime import datetime
from pydantic import BaseModel, Field

class PlanResponse(BaseModel):
    id: str
    name: str
    price: float
    months: int
    features: list[str]

class SubscribeRequest(BaseModel):
    plan_id: str

class SchoolSubscriptionResponse(BaseModel):
    plan_name: str
    status: str
    expires_at: datetime

class TopUpRequest(BaseModel):
    user_id: uuid.UUID
    amount: float = Field(gt=0)
    description: str | None = None

class TransactionResponse(BaseModel):
    id: uuid.UUID
    amount: float
    type: str
    description: str
    created_at: datetime
