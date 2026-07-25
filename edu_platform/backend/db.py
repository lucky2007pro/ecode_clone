"""
Asinxron PostgreSQL Ma\'lumotlar bazasi ulanishi (SQLAlchemy 2.0 asyncpg).
"""
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

DB_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:hojiakbar@localhost:5432/exode_db")

engine = create_async_engine(DB_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
