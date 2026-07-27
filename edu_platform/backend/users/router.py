from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from users.schema import UserCreate, UserResponse
from users.crud import get_user_by_email, create_user

router = APIRouter()


from fastapi.security import OAuth2PasswordRequestForm
from users.schema import TokenResponse
from users.auth import verify_password, create_access_token

from schools.crud import get_school_by_subdomain, create_school, create_user_school
from permissions.enums import Role
from schools.models import MembershipStatus

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bunday email allaqachon mavjud"
        )
    
    # Handle Role-based School Logic
    if user_in.role == Role.ADMIN:
        if not user_in.school_name or not user_in.subdomain:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin roliga maktab nomi va domeni kerak")
        
        school_exists = await get_school_by_subdomain(db, user_in.subdomain)
        if school_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu maktab domeni allaqachon band")
        
        # Create User
        new_user = await create_user(db, user_in)
        # Create School
        new_school = await create_school(db, user_in.school_name, user_in.subdomain, new_user.id)
        # Create UserSchool (Approved automatically for Admin)
        await create_user_school(db, new_user.id, new_school.id, MembershipStatus.APPROVED)
        
        return new_user

    else:
        # For non-admin, subdomain is required to know which school they are joining
        if not user_in.subdomain:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Maktab domanini kiriting")
            
        school = await get_school_by_subdomain(db, user_in.subdomain)
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday maktab domeni topilmadi")
            
        # Create User
        new_user = await create_user(db, user_in)
        # Create UserSchool (Pending for approval)
        await create_user_school(db, new_user.id, school.id, MembershipStatus.PENDING)
        
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
