"""
JWT Token yaratish va dekodlash (python-jose yordamida).
"""
import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.core.config import settings


def create_access_token(
    user_id: uuid.UUID,
    email: str,
    role: str,
    school_id: uuid.UUID,
    expires_delta: timedelta | None = None,
) -> str:
    """Access token yaratadi (default: 30 minut)."""
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "school_id": str(school_id),
        "exp": expire,
        "iat": now,
        "type": "access",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(user_id: uuid.UUID) -> tuple[str, datetime]:
    """Refresh token yaratadi (default: 7 kun)."""
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        "sub": str(user_id),
        "jti": str(uuid.uuid4()),
        "exp": expire,
        "iat": now,
        "type": "refresh",
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, expire


def decode_token(token: str) -> dict | None:
    """Tokenni tekshiradi va dekod qiladi."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
