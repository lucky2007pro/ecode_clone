"""
Course Service — kurslar, modullar, darslar, testlar, enrollment.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.models import Base
from app.api.courses import router as courses_router
from app.api.modules import router as modules_router
from app.api.lessons import router as lessons_router
from app.api.enrollments import router as enrollments_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Course Service",
    description="Kurslar, modullar, darslar va testlar boshqaruvi",
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

app.include_router(courses_router, prefix=f"{settings.API_PREFIX}/courses", tags=["courses"])
app.include_router(modules_router, prefix=f"{settings.API_PREFIX}/modules", tags=["modules"])
app.include_router(lessons_router, prefix=f"{settings.API_PREFIX}/lessons", tags=["lessons"])
app.include_router(enrollments_router, prefix=f"{settings.API_PREFIX}/enrollments", tags=["enrollments"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME}
