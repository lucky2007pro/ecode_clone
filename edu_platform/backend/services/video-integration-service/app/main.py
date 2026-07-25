"""
Video Integration Service — Kinescope API bilan integratsiya.
Video yuklash, webhook qabul qilish, tomosha statistikasi.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.models import Base
from app.api.uploads import router as uploads_router
from app.api.webhooks import router as webhooks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Video Integration Service",
    description="Kinescope video yuklash va boshqarish",
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

app.include_router(uploads_router, prefix=f"{settings.API_PREFIX}/videos", tags=["videos"])
app.include_router(webhooks_router, prefix=f"{settings.API_PREFIX}/webhooks/kinescope", tags=["webhooks"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME}
