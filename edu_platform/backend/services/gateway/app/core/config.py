"""
Gateway konfiguratsiyasi.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "gateway"
    DEBUG: bool = True

    # JWT (faqat token tekshirish uchun)
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"

    # Servislar URL'lari
    AUTH_SERVICE_URL: str = "http://localhost:8001"
    SCHOOL_SERVICE_URL: str = "http://localhost:8002"
    COURSE_SERVICE_URL: str = "http://localhost:8003"
    VIDEO_SERVICE_URL: str = "http://localhost:8004"
    CRM_SERVICE_URL: str = "http://localhost:8005"
    PAYMENT_SERVICE_URL: str = "http://localhost:8006"
    NOTIFICATION_SERVICE_URL: str = "http://localhost:8007"
    PROGRESS_SERVICE_URL: str = "http://localhost:8008"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()