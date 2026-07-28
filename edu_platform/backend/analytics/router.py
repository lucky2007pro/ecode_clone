from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_analytics(db: AsyncSession = Depends(get_db)):
    """Maktabning asosiy ko'rsatkichlari (MVP uchun mock qilingan)."""
    # Kelajakda DB dagi enrollments va users bo'yicha hisoblanadi
    return {
        "total_revenue": 12500000,
        "active_students": 142,
        "courses_count": 5,
        "completion_rate": 68,
        "monthly_data": [
            {"name": "Yan", "revenue": 1500000, "students": 20},
            {"name": "Fev", "revenue": 2800000, "students": 45},
            {"name": "Mar", "revenue": 4100000, "students": 85},
            {"name": "Apr", "revenue": 8500000, "students": 120},
            {"name": "May", "revenue": 12500000, "students": 142},
        ]
    }
