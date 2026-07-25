"""
Auth Service — ro'yxatdan o'tish, login, JWT/refresh token, rollar.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.models import Base
from app.api.auth import router as auth_router
from app.api.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: jadvallarni yaratish. Shutdown: engine'ni yopish."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Auth Service",
    description="Foydalanuvchilarni boshqarish va autentifikatsiya",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=f"{settings.API_PREFIX}/auth", tags=["auth"])
app.include_router(users_router, prefix=f"{settings.API_PREFIX}/users", tags=["users"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME}
