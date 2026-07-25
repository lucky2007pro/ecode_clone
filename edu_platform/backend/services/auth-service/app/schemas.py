"""
auth-service Pydantic sxemalari.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

from libs.shared_schemas.enums import UserRole


# --- USER SCHEMAS ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: str | None = None
    role: UserRole = UserRole.student


class UserCreate(UserBase):
    password: str
    school_id: uuid.UUID


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    school_id: uuid.UUID
    is_active: bool
    is_verified: bool
    created_at: datetime


# --- AUTH SCHEMAS ---
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str
