import uuid
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import get_db
from users.auth import SECRET_KEY, ALGORITHM
from users.crud import get_user_by_id
from schools.models import UserSchool, MembershipStatus
from .enums import Permission, ROLE_PERMISSIONS, Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """Tokenni tekshirib, joriy foydalanuvchini bazadan yuklaydi."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        user = await get_user_by_id(db, user_uuid)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


async def get_current_user_role(user=Depends(get_current_user)) -> Role:
    """Foydalanuvchi roli bazadan olinadi (JWT claim'ga ishonilmaydi)."""
    role = user.role
    if isinstance(role, Role):
        return role
    return Role(role)


async def get_current_user_school_id(token: str = Depends(oauth2_scheme)) -> str:
    """JWT ichidagi school_id claim'ini qaytaradi (legacy endpointlar uchun)."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        school_id = payload.get("school_id")
        if not school_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No school associated with this user")
        return school_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


async def get_current_school_id(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> uuid.UUID:
    """Tenant konteksti: foydalanuvchining tasdiqlangan a'zoligidan school_id olinadi."""
    res = await db.execute(
        select(UserSchool)
        .where(UserSchool.user_id == user.id)
        .where(UserSchool.status == MembershipStatus.APPROVED)
    )
    user_school = res.scalars().first()
    if not user_school:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Maktabga tasdiqlangan a'zolik topilmadi"
        )
    return user_school.school_id


class RequirePermissions:
    def __init__(self, required_permissions: List[Permission]):
        self.required_permissions = required_permissions

    async def __call__(self, user=Depends(get_current_user)):
        role = user.role
        if not isinstance(role, Role):
            role = Role(role)

        # Admin has all permissions
        if role == Role.ADMIN:
            return True

        user_permissions = ROLE_PERMISSIONS.get(role, [])

        for perm in self.required_permissions:
            if perm not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not enough permissions. Required: {perm.value}"
                )
        return True
