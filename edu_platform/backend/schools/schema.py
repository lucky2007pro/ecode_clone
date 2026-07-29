import uuid

from pydantic import BaseModel, ConfigDict

class SchoolCreate(BaseModel):

    name: str

    subdomain: str

    primary_color: str = "#6366f1"

class SchoolResponse(SchoolCreate):

    id: uuid.UUID

    custom_domain: str | None = None

    is_active: bool

    model_config = ConfigDict(from_attributes=True)

