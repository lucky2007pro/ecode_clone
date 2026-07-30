"""
Asinxron PostgreSQL Ma'lumotlar bazasi ulanishi (SQLAlchemy 2.0 asyncpg).
"""

import os

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.ext.asyncio import AsyncAttrs

DB_URL = os.getenv("DATABASE_URL")

if not DB_URL:

    raise RuntimeError("DATABASE_URL environment variable is required")

engine = create_async_engine(
    DB_URL,
    echo=os.getenv("DB_ECHO", "false").lower() == "true",
    future=True,
    pool_pre_ping=True,
    pool_recycle=300
)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):

    pass

async def init_db():

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:

    async with AsyncSessionLocal() as session:

        try:

            yield session

            await session.commit()

        except Exception:

            await session.rollback()

            raise

