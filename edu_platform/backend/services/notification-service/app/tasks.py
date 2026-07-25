"""
Notification Celery Tasks.
"""
import asyncio
from app.celery_app import celery_app
from app.channels.email import send_email
from app.channels.sms import send_sms


@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def send_welcome_email_task(self, email: str, full_name: str):
    """Yangi foydalanuvchiga xush kelibsiz emaili jo'natadi."""
    async def _send():
        subject = "Exode Platformasiga Xush Kelibsiz!"
        body = f"Assalomu alaykum, {full_name}! Platformamizdan muvaffaqiyatli ro'yxatdan o'tdingiz."
        await send_email(to_email=email, subject=subject, body=body)

    asyncio.run(_send())
