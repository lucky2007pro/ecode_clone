"""
crm-integration-service RabbitMQ event consumer'lari.
auth-service'dan "user.registered" kelganda Celery task'ini ishga tushiradi.
"""
import logging
from app.tasks import sync_user_to_kommo_task

logger = logging.getLogger("crm_event_consumer")


async def handle_user_registered_event(payload: dict):
    """user.registered hodisasi kelganda Celery navbatiga yuboradi."""
    data = payload.get("payload", {})
    user_id = data.get("user_id")
    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone")

    if user_id and email:
        logger.info(f"User registered event qabul qilindi: {email}. Celery navbatiga berilmoqda...")
        # Celery task'ini asinxron chaqirish (.delay)
        sync_user_to_kommo_task.delay(
            user_id_str=user_id,
            full_name=full_name or "Yangi O'quvchi",
            email=email,
            phone=phone,
        )
