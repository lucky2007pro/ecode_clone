"""
video-integration-service event publisher'lari.
"""
from app.core.config import settings
from libs.rabbitmq_client import RabbitMQPublisher
from libs.shared_schemas.events import BaseEvent

publisher = RabbitMQPublisher(settings.RABBITMQ_URL)


async def publish_video_ready(lesson_id: str, kinescope_video_id: str, duration_seconds: int | None):
    """Video kodlab bo'lingach, course-service'ga xabar berish uchun event yuboradi."""
    event = BaseEvent(
        event_type="video.ready",
        payload={
            "lesson_id": lesson_id,
            "kinescope_video_id": kinescope_video_id,
            "duration_seconds": duration_seconds,
        },
    )
    await publisher.publish(routing_key="video.ready", event=event)
