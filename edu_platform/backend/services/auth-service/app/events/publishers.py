"""
auth-service event publisher'lari.
"""
from app.core.config import settings
from libs.rabbitmq_client import RabbitMQPublisher
from libs.shared_schemas.events import BaseEvent

publisher = RabbitMQPublisher(settings.RABBITMQ_URL)


async def publish_user_registered(user_id: str, email: str, full_name: str, phone: str | None, school_id: str):
    """Foydalanuvchi ro'yxatdan o'tganda event yuboradi."""
    event = BaseEvent(
        event_type="user.registered",
        payload={
            "user_id": user_id,
            "email": email,
            "full_name": full_name,
            "phone": phone,
            "school_id": school_id,
        },
    )
    await publisher.publish(routing_key="user.registered", event=event)
