from collections import defaultdict

from fastapi import APIRouter, Depends

from sqlalchemy import select, func, case

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db

from courses.models import Course

from enrollments.models import Enrollment

from schools.models import UserSchool, MembershipStatus

from users.models import User

from permissions.dependencies import get_current_school_id

router = APIRouter()

@router.get("/dashboard")

async def get_dashboard_analytics(

    db: AsyncSession = Depends(get_db),

    school_id=Depends(get_current_school_id),

):

    people_query = (

        select(func.count(User.id), func.sum(case((User.is_active.is_(True), 1), else_=0)))

        .join(UserSchool, UserSchool.user_id == User.id)

        .where(UserSchool.school_id == school_id)

        .where(UserSchool.status == MembershipStatus.APPROVED)

    )

    total_people, active_people = (await db.execute(people_query)).one()

    total_people = total_people or 0

    active_people = active_people or 0

    completion_query = (

        select(

            func.sum(case((Enrollment.progress <= 0, 1), else_=0)),

            func.sum(case(((Enrollment.progress > 0) & (Enrollment.progress < 100), 1), else_=0)),

            func.sum(case(((Enrollment.progress >= 100) | (Enrollment.status == "completed"), 1), else_=0)),

        ).where(Enrollment.school_id == school_id)

    )

    not_started, in_progress, completed = (await db.execute(completion_query)).one()

    not_started, in_progress, completed = not_started or 0, in_progress or 0, completed or 0

    from sqlalchemy import literal_column

    month_expr = func.date_trunc("month", Enrollment.created_at).label("month")

    monthly_query = (

        select(month_expr, func.count(Enrollment.id))

        .where(Enrollment.school_id == school_id)

        .group_by(literal_column("month"))

        .order_by(literal_column("month"))

    )

    monthly = [

        {"name": month.strftime("%b").upper(), "value": count}

        for month, count in (await db.execute(monthly_query)).all()

    ]

    source_query = (

        select(Enrollment.source, func.count(Enrollment.id))

        .where(Enrollment.school_id == school_id)

        .group_by(Enrollment.source)

    )

    assignment_sources = [{"name": source or "self", "value": count} for source, count in (await db.execute(source_query)).all()]

    level_query = (

        select(User.level, func.count(User.id))

        .join(UserSchool, UserSchool.user_id == User.id)

        .where(UserSchool.school_id == school_id)

        .where(UserSchool.status == MembershipStatus.APPROVED)

        .group_by(User.level)

    )

    levels = [{"name": level or "junior", "value": count} for level, count in (await db.execute(level_query)).all()]

    top_query = (

        select(Course.id, Course.title, func.count(Enrollment.id).label("students_count"))

        .join(Enrollment, Enrollment.course_id == Course.id)

        .where(Course.school_id == school_id)

        .where(Enrollment.school_id == school_id)

        .group_by(Course.id, Course.title)

        .order_by(func.count(Enrollment.id).desc())

        .limit(5)

    )

    top_courses = [{"id": course_id, "name": title, "value": count} for course_id, title, count in (await db.execute(top_query)).all()]

    total_enrollments = not_started + in_progress + completed

    return {

        "metrics": {

            "people_count": total_people,

            "completed_count": completed,

            "active_percent": round(active_people * 100 / total_people) if total_people else 0,

        },

        "monthly_activity": monthly,

        "completion_status": {

            "not_started": round(not_started * 100 / total_enrollments) if total_enrollments else 0,

            "in_progress": round(in_progress * 100 / total_enrollments) if total_enrollments else 0,

            "completed": round(completed * 100 / total_enrollments) if total_enrollments else 0,

        },

        "assignment_sources": assignment_sources,

        "employee_levels": levels,

        "top_courses": top_courses,

    }

