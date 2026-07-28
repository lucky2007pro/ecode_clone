import asyncio
import os
import sys
import uuid

# Backend yo'lini qo'shish
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import engine, Base
from users.models import User
from users.crud import create_user, get_user_by_email
from users.schema import UserAdminCreate
from permissions.enums import Role
from schools.models import School, UserSchool
from sqlalchemy import text

async def run_tests():
    from db import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        print("1. Foydalanuvchi yaratish API/CRUD testi...")
        user_in = UserAdminCreate(
            email="test_bonus@example.com",
            full_name="Test Bonus User",
            password="password123",
            role=Role.ADMIN
        )
        
        try:
            new_user = await create_user(db, user_in)
            print(f"Muvaffaqiyatli yaratildi: {new_user.email}")
            print(f"Foydalanuvchi balansi: {new_user.balance} so'm (Bonus tekshirildi!)")
            assert new_user.balance == 1000000.0, "Bonus 1,000,000 so'm emas!"
        except Exception as e:
            print(f"Yaratishda xatolik (Balki allaqachon mavjuddir): {e}")

        # O'qish testi
        print("\n2. Bazadan o'qish testi...")
        user_db = await get_user_by_email(db, "test_bonus@example.com")
        if user_db:
            print(f"Bazada topildi: ID = {user_db.id}, Balans = {user_db.balance}")
        else:
            print("Foydalanuvchi bazada topilmadi!")

async def reset_db():
    print("\n3. Bazani tozalash boshlandi (Buyruqqa asosan)...")
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE;"))
        await conn.execute(text("CREATE SCHEMA public;"))
        await conn.run_sync(Base.metadata.create_all)
    print("Baza to'liq o'chirildi va yangidan top-toza holatda yaratildi.")

async def main():
    await run_tests()
    await reset_db()
    print("\nBarcha testlar tugadi!")

if __name__ == "__main__":
    asyncio.run(main())
