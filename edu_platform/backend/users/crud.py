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

from users.schema import UserUpdate

async def update_user(db: AsyncSession, user_obj: User, update_data: UserUpdate):

    if update_data.full_name is not None:

        user_obj.full_name = update_data.full_name

    if update_data.email is not None:

        user_obj.email = update_data.email

    if update_data.role is not None:

        user_obj.role = update_data.role

    if update_data.is_active is not None:

        user_obj.is_active = update_data.is_active

    if update_data.password is not None:

        user_obj.hashed_password = hash_password(update_data.password)

    await db.commit()

    await db.refresh(user_obj)

    return user_obj

