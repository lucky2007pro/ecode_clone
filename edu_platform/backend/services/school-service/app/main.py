"""
School Service — multi-tenant maktab boshqaruvi: sozlamalar, domen, tarif rejasi.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.models import Base
from app.api.schools import router as schools_router
from app.api.tariffs import router as tariffs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="School Service",
    description="Onlayn maktablarni boshqarish (multi-tenant)",
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

app.include_router(schools_router, prefix=f"{settings.API_PREFIX}/schools", tags=["schools"])
app.include_router(tariffs_router, prefix=f"{settings.API_PREFIX}/tariffs", tags=["tariffs"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME}
