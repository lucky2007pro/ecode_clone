import asyncio
import traceback
from sqlalchemy import text
from dotenv import load_dotenv
load_dotenv()
from db import get_db
from analytics.router import get_dashboard_analytics

async def main():
    try:
        async for db in get_db():
            res = await db.execute(text("SELECT id FROM schools LIMIT 1"))
            school_id = res.scalar()
            if not school_id:
                print("No school found")
                return
            
            print(f"Testing for school: {school_id}")
            # Patching the query just for the test to see if it works
            from enrollments.models import Enrollment
            from sqlalchemy import select, func, literal_column
            
            month_expr = func.date_trunc("month", Enrollment.created_at).label("month")
            monthly_query = (
                select(month_expr, func.count(Enrollment.id))
                .where(Enrollment.school_id == school_id)
                .group_by(literal_column("month"))
                .order_by(literal_column("month"))
            )
            res = await db.execute(monthly_query)
            print("Query successful:", res.all())
            break
    except Exception as e:
        print(f"Error occurred: {e}")
        traceback.print_exc()

asyncio.run(main())
