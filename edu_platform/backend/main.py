import os
from dotenv import load_dotenv
load_dotenv()  # .env dagi o'zgaruvchilarni birinchi navbatda yuklaymiz

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from redis_client import get_redis, close_redis

# DOMAIN ROUTERS
from users.router import router as users_router
from schools.router import router as schools_router
from courses.router import router as courses_router
from lessons.router import router as lessons_router
from enrollments.router import router as enrollments_router
from crm.router import router as crm_router
from payments.router import router as payments_router
from notifications.router import router as notifications_router
from homeworks.router import router as homeworks_router
from quizzes.router import router as quizzes_router
from analytics.router import router as analytics_router
from messages.router import router as messages_router
from marketing.router import router as marketing_router
from bot.router import router as bot_router
from api_keys.router import router as api_keys_router
from api_keys.router import saas_router
from videos.router import router as videos_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB sxemasi Alembic migratsiyalari orqali boshqariladi
    redis = await get_redis()
    await redis.ping()
    yield
    await close_redis()

app = FastAPI(
    title="Exode Education & ERP Platform API",
    description="Multi-tenant ERP va Ta'lim platformasi uchun Backend API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS sozlamalari — ruxsat berilgan originlar env orqali boshqariladi
ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerlarni ulash
app.include_router(users_router, prefix="/api/v1/users", tags=["Users & Authentication"])
app.include_router(schools_router, prefix="/api/v1/schools", tags=["Schools & Multi-Tenancy"])
app.include_router(courses_router, prefix="/api/v1/courses", tags=["Courses & E-learning"])
app.include_router(videos_router, prefix="/api/v1/videos", tags=["Kinescope Video Integration"])
app.include_router(crm_router, prefix="/api/v1/crm", tags=["Kommo CRM Integration"])
app.include_router(payments_router, prefix="/api/v1/payments", tags=["Telegram Admin Payments"])
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["Gmail Free SMTP Notifications"])
app.include_router(homeworks_router, prefix="/api/v1/homeworks", tags=["Homework & Practice Submissions"])
app.include_router(lessons_router, prefix="/api/v1/lessons", tags=["Lessons & Course Content"])
app.include_router(enrollments_router, prefix="/api/v1/enrollments", tags=["Student Enrollments"])
app.include_router(quizzes_router, prefix="/api/v1/quizzes", tags=["Quizzes & Tests"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics & Reporting"])
app.include_router(messages_router, prefix="/api/v1/messages", tags=["Chat & Messenger"])
app.include_router(marketing_router, prefix="/api/v1/marketing", tags=["Marketing & Sales"])
app.include_router(bot_router, prefix="/api/v1/bot", tags=["Telegram Bot"])
app.include_router(api_keys_router, prefix="/api/v1/keys", tags=["API Keys"])
app.include_router(saas_router, prefix="/saas", tags=["SaaS External API"])

# Serve uploaded videos statically
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/health", tags=["General"])
async def health():
    try:
        redis = await get_redis()
        await redis.ping()
        return {"status": "ok", "redis": "ok"}
    except Exception:
        return {"status": "degraded", "redis": "unavailable"}

# Ildiz endpoint
@app.get("/", tags=["General"])
async def root():
    return {
        "status": "success",
        "message": "Exode ERP Backend API ishlamoqda",
        "docs": "/docs",
        "version": app.version
    }
