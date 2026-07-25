import uuid
from pydantic import BaseModel

class VideoResponse(BaseModel):
    id: uuid.UUID
    kinescope_id: str
