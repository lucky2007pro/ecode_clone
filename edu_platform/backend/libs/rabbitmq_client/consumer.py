"""
RabbitMQ Event Consumer (aio-pika orqali asinxron).
Mikroservislar RabbitMQ'dagi eventlarni tinglash (subscribe) uchun shu moduldan foydalanadi.
"""
import json
import logging
from typing import Callable, Awaitable
import aio_pika

logger = logging.getLogger("rabbitmq_consumer")

EXCHANGE_NAME = "exode_events_exchange"


class RabbitMQConsumer:
    def __init__(self, rabbitmq_url: str, queue_name: str, routing_keys: list[str]):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.routing_keys = routing_keys
        self.connection: aio_pika.RobustConnection | None = None
        self.channel: aio_pika.RobustChannel | None = None

    async def start_listening(self, callback: Callable[[dict], Awaitable[None]]):
        """Navbatni eshitishni boshlaydi va event kelganda callback asinxron funksiyasini chaqiradi."""
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()

        # Prefetch count — bitta worker bir vaqtda nechta xabarni qayta ishlashi
        await self.channel.set_qos(prefetch_count=10)

        exchange = await self.channel.declare_exchange(
            EXCHANGE_NAME,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        # Servis uchun navbat (Queue) yaratish
        queue = await self.channel.declare_queue(self.queue_name, durable=True)

        # Routing key'larni navbatga bog'lash (Bind)
        for key in self.routing_keys:
            await queue.bind(exchange, routing_key=key)
            logger.info(f"Queue '{self.queue_name}' bound to routing_key '{key}'")

        async def process_message(message: aio_pika.IncomingMessage):
            async with message.process():
                try:
                    payload = json.loads(message.body.decode("utf-8"))
                    logger.info(f"Xabar qabul qilindi [{message.routing_key}]: {payload.get('event_id')}")
                    await callback(payload)
                except Exception as e:
                    logger.error(f"Xabarni qayta ishlashda xatolik: {e}", exc_info=True)
                    # Re-queue qilish yoki Dead Letter Exchange'ga yuborish mumkin

        logger.info(f"[{self.queue_name}] Navbati eventlarni eshitishni boshladi...")
        await queue.consume(process_message)

    async def close(self):
        """Ulanishni yopadi."""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
