from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from users.schema import UserCreate, UserResponse
from users.crud import get_user_by_email, create_user

router = APIRouter()


from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from users.schema import TokenResponse
from users.auth import verify_password, create_access_token

from schools.crud import get_school_by_subdomain, create_school, create_user_school
from permissions.enums import Role
from schools.models import MembershipStatus

import json
from redis_client import get_redis
from notifications.email import send_email_otp
from users.schema import UserRegisterVerify, UserAdminCreate
from permissions.dependencies import RequirePermissions, get_current_user_role
from permissions.enums import Permission

@router.post("/register/send-otp")
async def send_registration_otp(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bunday email allaqachon mavjud"
        )
    
    if user_in.role == Role.ADMIN:
        if not user_in.school_name or not user_in.subdomain:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin roliga maktab nomi va domeni kerak")
        school_exists = await get_school_by_subdomain(db, user_in.subdomain)
        if school_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu maktab domeni allaqachon band")
    else:
        if not user_in.subdomain:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Maktab domanini kiriting")
        school = await get_school_by_subdomain(db, user_in.subdomain)
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday maktab domeni topilmadi")

    # Ma'lumotlarni Redisga vaqtincha saqlab, OTP jo'natamiz
    otp_code = await send_email_otp(user_in.email)
    
    redis = await get_redis()
    # OTP ni saqlaymiz (5 daqiqa)
    await redis.setex(f"otp:{user_in.email}", 300, otp_code)
    # Form data ni ham saqlab qo'yamiz (parol heshlanmagan holatda, lekin bu vaqtincha)
    await redis.setex(f"reg_data:{user_in.email}", 300, user_in.model_dump_json())
    
    return {"message": "Tasdiqlash kodi elektron pochtangizga yuborildi."}

@router.post("/register/verify", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def verify_registration_otp(verify_in: UserRegisterVerify, db: AsyncSession = Depends(get_db)):
    redis = await get_redis()
    saved_otp = await redis.get(f"otp:{verify_in.email}")
    
    if not saved_otp or str(saved_otp) != str(verify_in.otp_code).strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP kod noto'g'ri yoki muddati o'tgan")
        
    saved_data_str = await redis.get(f"reg_data:{verify_in.email}")
    if not saved_data_str:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ro'yxatdan o'tish ma'lumotlari topilmadi, boshidan boshlang")
        
    user_data = UserCreate.model_validate_json(saved_data_str)
    
    if user_data.role == Role.ADMIN:
        new_user = await create_user(db, user_data)
        new_school = await create_school(db, user_data.school_name, user_data.subdomain, new_user.id)
        await create_user_school(db, new_user.id, new_school.id, MembershipStatus.APPROVED)
    else:
        school = await get_school_by_subdomain(db, user_data.subdomain)
        new_user = await create_user(db, user_data)
        await create_user_school(db, new_user.id, school.id, MembershipStatus.PENDING)

    # Kod ishlatilgach o'chiramiz
    await redis.delete(f"otp:{verify_in.email}")
    await redis.delete(f"reg_data:{verify_in.email}")

    return new_user

from jose import jwt
from users.auth import SECRET_KEY, ALGORITHM

async def get_current_school_id(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("school_id")

@router.post("/admin-create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_user(
    user_in: UserAdminCreate, 
    db: AsyncSession = Depends(get_db),
    has_perm: bool = Depends(RequirePermissions([Permission.MANAGE_USERS])),
    school_id: str = Depends(get_current_school_id)
):
    if not school_id:
        raise HTTPException(status_code=403, detail="Maktabingiz topilmadi")
        
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Bunday email allaqachon mavjud")
        
    # Parol bilan o'quvchi yaratish
    new_user = await create_user(db, user_in)
    import uuid
    # To'g'ridan to'g'ri maktabga qabul qilish
    await create_user_school(db, new_user.id, uuid.UUID(school_id), MembershipStatus.APPROVED)
    return new_user

from sqlalchemy import select
from schools.models import UserSchool, MembershipStatus

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user belongs to a school and is approved
    res = await db.execute(
        select(UserSchool)
        .where(UserSchool.user_id == user.id)
        .where(UserSchool.status == MembershipStatus.APPROVED)
    )
    user_school = res.scalars().first()
    
    if not user_school:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hisobingiz hali tasdiqlanmagan yoki hech qanday maktabga a'zo emassiz"
        )

    access_token = create_access_token(user_id=str(user.id), role=user.role.value, school_id=str(user_school.school_id))
    return {"access_token": access_token, "token_type": "bearer"}

from permissions.dependencies import get_current_user

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user = Depends(get_current_user)):
    """Tizimga kirgan foydalanuvchining ma'lumotlarini qaytaradi."""
    return current_user
