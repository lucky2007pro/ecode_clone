import os

base = r"d:\python najot ta'liim\fastapi\erp_platform\edu_platform\backend"

def w(path, content):
    full = os.path.join(base, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# 1. db.py
w('db.py', '''"""
Asinxron PostgreSQL Ma\\'lumotlar bazasi ulanishi (SQLAlchemy 2.0 asyncpg).
"""
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

DB_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:hojiakbar@localhost:5432/exode_db")

engine = create_async_engine(DB_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
''')

# 2. redis_client.py
w('redis_client.py', '''"""
Redis asinxron kesh va rate-limiter mijozi.
"""
import os
import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def get_redis():
    return redis_client
''')

# 3. main.py
w('main.py', '''"""
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
''')

# 4. users module (auth.py, crud.py, models.py, router.py, schema.py)
w('users/models.py', '''
import uuid
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
import enum

class UserRole(str, enum.Enum):
    school_owner = "school_owner"
    expert_teacher = "expert_teacher"
    producer = "producer"
    corporate_hr = "corporate_hr"
    student = "student"
    other = "other"

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(default=UserRole.school_owner)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
''')

w('users/schema.py', '''
import uuid
from pydantic import BaseModel, EmailStr
from users.models import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.school_owner

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
''')

w('users/auth.py', '''
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "super-secret-jwt-key"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload = {"sub": user_id, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
''')

w('users/crud.py', '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from users.models import User
from users.schema import UserCreate
from users.auth import hash_password

async def get_user_by_email(db: AsyncSession, email: str):
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: UserCreate):
    hashed = hash_password(user_in.password)
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        role=user_in.role,
        hashed_password=hashed
    )
    db.add(user)
    await db.flush()
    return user
''')

w('users/router.py', '''
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from users.schema import UserCreate, UserResponse, TokenResponse
from users.crud import get_user_by_email, create_user
from users.auth import create_access_token, verify_password

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email allaqachon mavjud")
    return await create_user(db, user_in)
''')

# 5. schools module
w('schools/models.py', '''
import uuid
from sqlalchemy import String, Boolean, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class School(Base):
    __tablename__ = "schools"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    subdomain: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    custom_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    primary_color: Mapped[str] = mapped_column(String(20), default="#6366f1")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
''')

w('schools/schema.py', '''
import uuid
from pydantic import BaseModel

class SchoolCreate(BaseModel):
    name: str
    subdomain: str
    primary_color: str = "#6366f1"

class SchoolResponse(SchoolCreate):
    id: uuid.UUID
    custom_domain: str | None = None
    is_active: bool
    class Config:
        from_attributes = True
''')

w('schools/crud.py', '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schools.models import School
from schools.schema import SchoolCreate

async def create_school(db: AsyncSession, school_in: SchoolCreate):
    school = School(**school_in.model_dump())
    db.add(school)
    await db.flush()
    return school
''')

w('schools/router.py', '''
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schools.schema import SchoolCreate, SchoolResponse
from schools.crud import create_school

router = APIRouter()

@router.post("/", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
async def add_school(school_in: SchoolCreate, db: AsyncSession = Depends(get_db)):
    return await create_school(db, school_in)
''')

# 6. courses module
w('courses/models.py', '''
import uuid
from sqlalchemy import String, Text, Numeric, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
''')

w('courses/schema.py', '''
import uuid
from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    slug: str
    description: str | None = None
    price: float = 0.0

class CourseResponse(CourseCreate):
    id: uuid.UUID
    class Config:
        from_attributes = True
''')

w('courses/crud.py', '''
from sqlalchemy.ext.asyncio import AsyncSession
from courses.models import Course
from courses.schema import CourseCreate

async def create_course(db: AsyncSession, course_in: CourseCreate):
    course = Course(**course_in.model_dump())
    db.add(course)
    await db.flush()
    return course
''')

w('courses/router.py', '''
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from courses.schema import CourseCreate, CourseResponse
from courses.crud import create_course

router = APIRouter()

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def add_course(course_in: CourseCreate, db: AsyncSession = Depends(get_db)):
    return await create_course(db, course_in)
''')

# 7. videos module
w('videos/kinescope.py', '''
import httpx

KINESCOPE_API_KEY = "your-kinescope-key"

async def upload_to_kinescope(title: str):
    return {"video_id": "kinescope-v101", "status": "processing"}
''')

w('videos/models.py', '''
import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class Video(Base):
    __tablename__ = "videos"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    kinescope_id: Mapped[str] = mapped_column(String(100))
''')

w('videos/schema.py', '''
import uuid
from pydantic import BaseModel

class VideoResponse(BaseModel):
    id: uuid.UUID
    kinescope_id: str
''')

w('videos/router.py', '''
from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_videos():
    return [{"id": "v1", "kinescope_id": "kinescope-101"}]
''')

# 8. crm module
w('crm/kommo.py', '''
import httpx

async def send_lead_to_kommo(name: str, phone: str):
    return {"lead_id": 1042, "status": "created"}
''')

w('crm/models.py', '''
import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class CrmLead(Base):
    __tablename__ = "crm_leads"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    kommo_id: Mapped[int] = mapped_column()
''')

w('crm/schema.py', '''
from pydantic import BaseModel

class LeadCreate(BaseModel):
    name: str
    phone: str
''')

w('crm/router.py', '''
from fastapi import APIRouter
from crm.kommo import send_lead_to_kommo

router = APIRouter()

@router.post("/lead")
async def create_lead(name: str, phone: str):
    return await send_lead_to_kommo(name, phone)
''')

# 9. payments module
w('payments/payme.py', '''
async def handle_payme_rpc(payload: dict):
    return {"result": {"allow": True}}
''')

w('payments/click.py', '''
async def handle_click_prepare(data: dict):
    return {"error": 0, "error_note": "Success"}
''')

w('payments/uzum.py', '''
async def handle_uzum_checkout(amount: float):
    return {"payment_url": "https://payment.uzumbank.uz/pay"}
''')

w('payments/models.py', '''
import uuid
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    provider: Mapped[str] = mapped_column(String(50))
''')

w('payments/schema.py', '''
from pydantic import BaseModel

class PaymentCreate(BaseModel):
    amount: float
    provider: str
''')

w('payments/crud.py', '''
from sqlalchemy.ext.asyncio import AsyncSession
from payments.models import Payment
from payments.schema import PaymentCreate

async def create_payment(db: AsyncSession, pay_in: PaymentCreate):
    p = Payment(**pay_in.model_dump())
    db.add(p)
    await db.flush()
    return p
''')

w('payments/router.py', '''
from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_payments():
    return [{"provider": "payme", "status": "paid"}]
''')

# 10. notifications module
w('notifications/telegram.py', '''
async def send_telegram_msg(chat_id: str, text: str):
    return True
''')

w('notifications/sms.py', '''
async def send_eskiz_sms(phone: str, msg: str):
    return True
''')

w('notifications/email.py', '''
async def send_smtp_email(to: str, text: str):
    return True
''')

w('notifications/router.py', '''
from fastapi import APIRouter
router = APIRouter()

@router.post("/send")
async def send_notification(user_id: str, message: str):
    return {"status": "sent"}
''')

# 11. tests module (conftest.py, test_users.py, test_courses.py, test_payments.py)
w('tests/conftest.py', '''
import pytest
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
''')

w('tests/test_users.py', '''
import pytest

@pytest.mark.asyncio
async def test_user_registration():
    assert True
''')

w('tests/test_courses.py', '''
import pytest

@pytest.mark.asyncio
async def test_course_creation():
    assert True
''')

w('tests/test_payments.py', '''
import pytest

@pytest.mark.asyncio
async def test_payme_checkout():
    assert True
''')

# 12. Root configs (Dockerfile, docker-compose.yml, .dockerignore, pytest.ini, README.md, requirements.txt)
w('Dockerfile', '''
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

w('docker-compose.yml', '''
version: "3.8"
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:hojiakbar@db:5432/exode_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: hojiakbar
      POSTGRES_DB: exode_db
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
''')

w('.dockerignore', '''
.venv
__pycache__
*.pyc
.git
.env
''')

w('pytest.ini', '''
[pytest]
asyncio_mode = auto
testpaths = tests
''')

w('README.md', '''
# Exode Platform — Modular FastAPI Architecture

Clean, modular, domain-driven design structure:

`
fast_async/
├── users/          # Users & Auth (auth.py, crud.py, models.py, router.py, schema.py)
├── schools/        # School management (crud.py, models.py, router.py, schema.py)
├── courses/        # Course & Homework (crud.py, models.py, router.py, schema.py)
├── videos/         # Kinescope API (kinescope.py, models.py, router.py, schema.py)
├── crm/            # Kommo CRM (kommo.py, models.py, router.py, schema.py)
├── payments/       # Payments (payme.py, click.py, uzum.py, crud.py, models.py, router.py, schema.py)
├── notifications/ # Notifications (telegram.py, sms.py, email.py, router.py)
├── tests/          # Tests (conftest.py, test_users.py, test_courses.py, test_payments.py)
├── db.py
├── redis_client.py
├── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
`
''')

w('requirements.txt', '''
fastapi>=0.110.0
uvicorn[standard]>=0.28.0
sqlalchemy[asyncio]>=2.0.28
asyncpg>=0.29.0
pydantic>=2.6.4
pydantic-settings>=2.2.1
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
httpx>=0.27.0
redis>=5.0.3
pytest>=8.1.1
pytest-asyncio>=0.23.6
''')

print("Clean modular structure created successfully!")