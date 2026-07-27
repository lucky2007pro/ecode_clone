from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from users.schema import UserCreate, UserResponse
from users.crud import get_user_by_email, create_user

router = APIRouter()


from fastapi.security import OAuth2PasswordRequestForm
from users.schema import TokenResponse
from users.auth import verify_password, create_access_token

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bunday email allaqachon mavjud"
        )
    return await create_user(db, user_in)

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user_id=str(user.id), role=user.role.value)
    return {"access_token": access_token, "token_type": "bearer"}
