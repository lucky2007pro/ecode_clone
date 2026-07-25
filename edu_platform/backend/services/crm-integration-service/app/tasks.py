"""
Celery Task'lari: Kommo API 7 req/sec limitiga tushmaslik uchun rate_limit="5/s" bilan ishlaydi.
"""
import asyncio
import uuid
import logging
from sqlalchemy import select
from app.celery_app import celery_app
from app.core.database import async_session_maker
from app.models import CrmLead, CrmSyncLog
from app.kommo_client import kommo_client
from libs.shared_schemas.enums import CrmSyncStatus

logger = logging.getLogger("crm_tasks")


@celery_app.task(
    bind=True,
    max_retries=5,
    default_retry_delay=10,
    rate_limit="5/s",  # Kommo API limitidan ko'p emas (max 7 req/sec)
)
def sync_user_to_kommo_task(self, user_id_str: str, full_name: str, email: str, phone: str | None = None):
    """
    Foydalanuvchi ro'yxatdan o'tganda Kommo'ga lid sifatida yuboruvchi Celery Task.
    """
    async def _async_sync():
        user_id = uuid.UUID(user_id_str)
        async with async_session_maker() as db:
            # DB da bormi tekshirish
            stmt = select(CrmLead).where(CrmLead.user_id == user_id)
            res = await db.execute(stmt)
            crm_lead = res.scalar_one_or_none()

            if not crm_lead:
                crm_lead = CrmLead(user_id=user_id, sync_status=CrmSyncStatus.pending)
                db.add(crm_lead)
                await db.flush()

            try:
                result = await kommo_client.create_lead_complex(full_name=full_name, email=email, phone=phone)
                crm_lead.kommo_lead_id = result.get("kommo_lead_id")
                crm_lead.kommo_contact_id = result.get("kommo_contact_id")
                crm_lead.sync_status = CrmSyncStatus.synced

                # Log
                log = CrmSyncLog(
                    lead_id=crm_lead.id,
                    event_type="lead.created",
                    direction="outbound",
                    payload={"full_name": full_name, "email": email, "phone": phone},
                    status=CrmSyncStatus.synced,
                )
                db.add(log)
                await db.commit()
                logger.info(f"User {user_id} Kommo'ga muvaffaqiyatli sinxronlandi. Lead ID: {crm_lead.kommo_lead_id}")

            except Exception as exc:
                crm_lead.sync_status = CrmSyncStatus.failed
                log = CrmSyncLog(
                    lead_id=crm_lead.id,
                    event_type="lead.created",
                    direction="outbound",
                    payload={"full_name": full_name, "email": email},
                    status=CrmSyncStatus.failed,
                    error_message=str(exc),
                )
                db.add(log)
                await db.commit()
                # Taskni qayta urinishga yuborish
                raise self.retry(exc=exc)

    asyncio.run(_async_sync())
