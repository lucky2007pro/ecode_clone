"""
crm-integration-service Pydantic sxemalari.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from libs.shared_schemas.enums import CrmSyncStatus


class CrmLeadCreate(BaseModel):
    user_id: uuid.UUID
    full_name: str
    email: str
    phone: str | None = None


class KommoWebhookPayload(BaseModel):
    account_id: str | None = None
    leads: dict | list | None = None


class CrmLeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    kommo_lead_id: str | None
    kommo_contact_id: str | None
    pipeline_status: str | None
    sync_status: CrmSyncStatus
    created_at: datetime
