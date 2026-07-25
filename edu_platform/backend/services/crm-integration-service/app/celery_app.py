"""
Celery App konfiguratsiyasi (crm_queue navbati).
"""
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "crm_integration_service",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_default_queue="crm_queue",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
