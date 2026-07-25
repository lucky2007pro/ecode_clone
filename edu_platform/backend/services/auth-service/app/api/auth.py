"""
Auth API router'lar (Register, Login, Refresh).
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import UserCreate, UserLogin, UserResponse, TokenResponse, RefreshTokenRequest
from app.services.auth_service import register_user, login_user, refresh_access_token

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """Yangi foydalanuvchini ro'yxatdan o'tkazadi."""
    return await register_user(db, user_in)


@router.post("/login", response_model=TokenResponse)
async def login(login_in: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login qiladi va JWT token beradi."""
    return await login_user(db, login_in)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(req: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """Refresh token orqali access tokenni yangilaydi."""
    return await refresh_access_token(db, req)
