"""
RabbitMQ Event Publisher (aio-pika orqali asinxron).
Barcha mikroservislar eventlarni RabbitMQ exchange'iga yuborish uchun shu moduldan foydalanadi.
"""
import json
import logging
import aio_pika

from libs.shared_schemas.events import BaseEvent

logger = logging.getLogger("rabbitmq_publisher")

EXCHANGE_NAME = "exode_events_exchange"


class RabbitMQPublisher:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection: aio_pika.RobustConnection | None = None
        self.channel: aio_pika.RobustChannel | None = None
        self.exchange: aio_pika.RobustExchange | None = None

    async def connect(self):
        """RabbitMQ serveriga barqaror (robust) ulanadi."""
        if not self.connection or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
            self.channel = await self.connection.channel()
            # Topic turidagi exchange yaratamiz
            self.exchange = await self.channel.declare_exchange(
                EXCHANGE_NAME,
                type=aio_pika.ExchangeType.TOPIC,
                durable=True,
            )
            logger.info("RabbitMQ Publisher muvaffaqiyatli ulandi.")

    async def publish(self, routing_key: str, event: BaseEvent):
        """Eventni tegishli routing_key bilan RabbitMQ'ga yuboradi."""
        await self.connect()

        message_body = event.model_dump_json().encode("utf-8")
        message = aio_pika.Message(
            body=message_body,
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,  # Diskda saqlash
        )

        assert self.exchange is not None
        await self.exchange.publish(message, routing_key=routing_key)
        logger.info(f"Event yuborildi: routing_key='{routing_key}', event_id='{event.event_id}'")

    async def close(self):
        """Ulanishni yopadi."""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            logger.info("RabbitMQ Publisher ulanishi yopildi.")
