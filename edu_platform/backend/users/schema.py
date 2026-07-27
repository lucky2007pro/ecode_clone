import uuid
from pydantic import BaseModel, EmailStr
from permissions.enums import Role

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Role = Role.STUDENT

class UserCreate(UserBase):
    password: str
    school_name: str | None = None
    subdomain: str | None = None

class UserRegisterVerify(UserCreate):
    otp_code: str

class UserAdminCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
