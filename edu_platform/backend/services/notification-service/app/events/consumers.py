"""
notification-service RabbitMQ event consumer.
"user.registered" kabi hodisalarga quloq soladi.
"""
from app.tasks import send_welcome_email_task


async def handle_notification_events(payload: dict):
    event_type = payload.get("event_type")
    data = payload.get("payload", {})

    if event_type == "user.registered":
        email = data.get("email")
        full_name = data.get("full_name")
        if email:
            send_welcome_email_task.delay(email=email, full_name=full_name or "Foydalanuvchi")
