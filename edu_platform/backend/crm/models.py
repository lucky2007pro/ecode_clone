import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class CrmLead(Base):
    __tablename__ = "crm_leads"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    kommo_id: Mapped[int] = mapped_column()
