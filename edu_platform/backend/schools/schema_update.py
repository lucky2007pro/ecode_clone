import { BaseModel } from 'pydantic'
from typing import Optional

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    custom_domain: Optional[str] = None
    primary_color: Optional[str] = None
