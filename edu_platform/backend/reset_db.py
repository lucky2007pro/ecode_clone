import asyncio
import os
import sys

# Backend yo'lini qo'shish
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import engine, Base
from users.models import User
from schools.models import School, UserSchool
from courses.models import Course
from sqlalchemy import text

async def reset_db():
    print("Bazani tozalash boshlandi...")
    async with engine.begin() as conn:
        # Hamma jadvallarni o'chirish (Cascade)
        await conn.execute(text("DROP SCHEMA public CASCADE;"))
        await conn.execute(text("CREATE SCHEMA public;"))
        # Jadvallarni boshqatdan yaratish
        await conn.run_sync(Base.metadata.create_all)
    print("Baza tozalandi va jadvallar yangidan yaratildi (balance ustuni bilan).")

async def main():
    await reset_db()
    print("Barcha jadvallar muvaffaqiyatli tiklandi.")

if __name__ == "__main__":
    asyncio.run(main())
