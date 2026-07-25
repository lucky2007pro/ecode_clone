"""
notification-service Pydantic sxemalari.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NotificationSendRequest(BaseModel):
    user_id: uuid.UUID
    channel: str  # "email" | "sms" | "push"
    template_code: str
    params: dict = {}


class NotificationTemplateCreate(BaseModel):
    code: str
    channel: str
    subject: str | None = None
    body: str


class NotificationTemplateResponse(NotificationTemplateCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
