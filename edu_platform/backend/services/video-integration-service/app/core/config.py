"""
video-integration-service konfiguratsiyasi.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "video-integration-service"
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

    # Kinescope API
    KINESCOPE_API_TOKEN: str = "your-kinescope-token-here"
    KINESCOPE_API_URL: str = "https://api.kinescope.io/v1"
    KINESCOPE_UPLOADER_URL: str = "https://uploader.kinescope.io/v2/video"

    # RabbitMQ & Redis
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()