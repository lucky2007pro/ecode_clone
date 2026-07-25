"""
FastAPI Asosiy Ilova (Main Entrypoint).
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import engine, Base
from users.router import router as users_router
from schools.router import router as schools_router
from courses.router import router as courses_router
from videos.router import router as videos_router
from crm.router import router as crm_router
from payments.router import router as payments_router
from notifications.router import router as notifications_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Exode Platform API",
    description="FastAPI Clean Modular Architecture matching user design",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/api/v1/users", tags=["Users & Auth"])
app.include_router(schools_router, prefix="/api/v1/schools", tags=["Schools"])
app.include_router(courses_router, prefix="/api/v1/courses", tags=["Courses & Homework"])
app.include_router(videos_router, prefix="/api/v1/videos", tags=["Kinescope Videos"])
app.include_router(crm_router, prefix="/api/v1/crm", tags=["Kommo CRM"])
app.include_router(payments_router, prefix="/api/v1/payments", tags=["Payments & Installments"])
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["Notifications"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "Exode Platform"}
