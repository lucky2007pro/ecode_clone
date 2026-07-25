"""
crm-integration-service konfiguratsiyasi.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "crm-integration-service"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "hojiakbar"
    DB_NAME: str = "exode_db"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Kommo (amoCRM) API
    KOMMO_SUBDOMAIN: str = "exode"
    KOMMO_LONG_LIVED_TOKEN: str = "your-kommo-long-lived-token-here"

    @property
    def KOMMO_API_URL(self) -> str:
        return f"https://{self.KOMMO_SUBDOMAIN}.kommo.com/api/v4"

    # Celery & RabbitMQ & Redis
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()