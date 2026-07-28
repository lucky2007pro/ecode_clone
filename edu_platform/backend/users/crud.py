from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from users.models import User
from users.schema import UserCreate
from users.auth import hash_password


async def get_user_by_email(db: AsyncSession, email: str):
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id):
    res = await db.execute(select(User).where(User.id == user_id))
    return res.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: UserCreate):
    hashed = hash_password(user_in.password)
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        role=user_in.role,
        hashed_password=hashed
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
