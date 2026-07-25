"""
Auth ish mantiqiy servisi (Register, Login, Refresh Token).
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models import User, RefreshToken
from app.schemas import UserCreate, UserLogin, TokenResponse, RefreshTokenRequest
from app.services.password import hash_password, verify_password
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.events.publishers import publish_user_registered


async def register_user(db: AsyncSession, user_in: UserCreate) -> User:
    """Yangi foydalanuvchini ro'yxatdan o'tkazish."""
    # Email mavjudligini tekshirish
    stmt = select(User).where(User.email == user_in.email)
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bunday email allaqachon ro'yxatdan o'tgan",
        )

    db_user = User(
        email=user_in.email,
        phone=user_in.phone,
        password_hash=hash_password(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role,
        school_id=user_in.school_id,
    )
    db.add(db_user)
    await db.flush()

    # Eventni RabbitMQ'ga yuborish (Kommo CRM va Notification servislar tinglaydi)
    try:
        await publish_user_registered(
            user_id=str(db_user.id),
            email=db_user.email,
            full_name=db_user.full_name,
            phone=db_user.phone,
            school_id=str(db_user.school_id),
        )
    except Exception:
        # Event yuborishda xatolik bo'lsa ham registratsiya to'xtab qolmasligi uchun log qilamiz
        pass

    return db_user


async def login_user(db: AsyncSession, login_in: UserLogin) -> TokenResponse:
    """Foydalanuvchi tizimga kirishi va token olishi."""
    stmt = select(User).where(User.email == login_in.email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not verify_password(login_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Foydalanuvchi hisobi faol emas",
        )

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        role=user.role.value,
        school_id=user.school_id,
    )
    refresh_token_str, expires_at = create_refresh_token(user_id=user.id)

    # Refresh tokenni bazada saqlash
    db_refresh = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=expires_at,
    )
    db.add(db_refresh)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_str,
    )


async def refresh_access_token(db: AsyncSession, req: RefreshTokenRequest) -> TokenResponse:
    """Refresh token orqali yangi access token olish."""
    payload = decode_token(req.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yaroqsiz refresh token",
        )

    user_id = uuid.UUID(payload.get("sub"))
    
    # Bazadan tokenni va foydalanuvchini izlash
    stmt = select(RefreshToken).where(
        RefreshToken.token == req.refresh_token,
        RefreshToken.revoked == False,
    )
    res = await db.execute(stmt)
    token_obj = res.scalar_one_or_none()

    if not token_obj or token_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token muddati o'tgan yoki bekor qilingan",
        )

    user_stmt = select(User).where(User.id == user_id)
    user_res = await db.execute(user_stmt)
    user = user_res.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi")

    # Eski tokenni bekor qilish (Revoke)
    token_obj.revoked = True

    # Yangi juftlik yaratish
    new_access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        role=user.role.value,
        school_id=user.school_id,
    )
    new_refresh_str, new_expires = create_refresh_token(user_id=user.id)

    new_token_obj = RefreshToken(
        user_id=user.id,
        token=new_refresh_str,
        expires_at=new_expires,
    )
    db.add(new_token_obj)

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_str,
    )
