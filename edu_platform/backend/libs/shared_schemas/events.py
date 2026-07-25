"""
RabbitMQ Event formatlari (Pydantic).
Barcha mikroservislar RabbitMQ'da umumiy event formati orqali muloqot qiladi.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    event_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    payload: dict
