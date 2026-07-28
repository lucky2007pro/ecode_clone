import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from homeworks.models import HomeworkSubmission
from homeworks.schema import HomeworkSubmissionCreate, GradeRequest


async def submit_homework(db: AsyncSession, sub_in: HomeworkSubmissionCreate):
    submission = HomeworkSubmission(**sub_in.model_dump())
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    return submission


async def get_all_submissions(db: AsyncSession):
    res = await db.execute(select(HomeworkSubmission))
    return res.scalars().all()


async def get_lesson_submissions(db: AsyncSession, lesson_id: uuid.UUID):
    res = await db.execute(select(HomeworkSubmission).where(HomeworkSubmission.lesson_id == lesson_id))
    return res.scalars().all()


async def get_student_submissions(db: AsyncSession, student_id: uuid.UUID):
    res = await db.execute(select(HomeworkSubmission).where(HomeworkSubmission.student_id == student_id))
    return res.scalars().all()


async def grade_submission(db: AsyncSession, sub_id: uuid.UUID, grade_in: GradeRequest):
    res = await db.execute(select(HomeworkSubmission).where(HomeworkSubmission.id == sub_id))
    submission = res.scalar_one_or_none()
    if submission:
        submission.grade = grade_in.grade
        submission.status = grade_in.status
        submission.feedback = grade_in.feedback
        await db.commit()
        await db.refresh(submission)
    return submission
