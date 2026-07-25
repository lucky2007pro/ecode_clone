"""
Umumiy JWT tekshirish middleware va dependency'lar.
Barcha mikroservislar va Gateway foydalanuvchini identifikatsiya qilish uchun
shu moduldan foydalanadi.
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security_scheme = HTTPBearer()

SECRET_KEY = "super-secret-key-change-in-production"
ALGORITHM = "HS256"


class CurrentUser:
    """JWT dekod qilingan foydalanuvchi ma'lumotlari."""
    def __init__(self, user_id: str, email: str, role: str, school_id: str):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.school_id = school_id


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)]
) -> CurrentUser:
    """JWT token validatsiyasi va foydalanuvchini olish."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        school_id: str = payload.get("school_id")
        
        if not user_id or payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Yaroqsiz auth token",
            )
            
        return CurrentUser(user_id=user_id, email=email, role=role, school_id=school_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token muddati o'tgan yoki yaroqsiz",
        )
