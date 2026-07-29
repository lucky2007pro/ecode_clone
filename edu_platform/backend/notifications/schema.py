import uuid

from datetime import datetime

from typing import List, Optional

from pydantic import BaseModel, ConfigDict

class NotificationResponse(BaseModel):

    id: uuid.UUID

    title: str

    body: Optional[str] = None

    is_read: bool

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NotificationListResponse(BaseModel):

    unread_count: int

    results: List[NotificationResponse]

