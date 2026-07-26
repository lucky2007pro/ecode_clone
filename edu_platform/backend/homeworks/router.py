from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

class HomeworkSubmission(BaseModel):
    id: int
    student_name: str
    course_title: str
    lesson_title: str
    submission_text: str
    status: str  # "Sent for Review", "Approved", "Rejected"
    grade: Optional[int] = None
    feedback: Optional[str] = None
    submitted_at: str

class GradeRequest(BaseModel):
    submission_id: int
    grade: int
    status: str
    feedback: str

# IN-MEMORY / DB HOMEWORK SUBMISSIONS DEMO STORE
FAKE_SUBMISSIONS = [
    {
        "id": 101,
        "student_name": "Sardor Alimov",
        "course_title": "Python & FastAPI Microservices",
        "lesson_title": "1.1 asyncpg DB Connection Setup",
        "submission_text": "Github repo: github.com/sardor/fastapi_db_hw. SQL mashqlarini bajarib database init_db scriptini yozdim.",
        "status": "Sent for Review",
        "grade": None,
        "feedback": None,
        "submitted_at": "Bugun, 14:20"
    },
    {
        "id": 102,
        "student_name": "Jasur Bekmurodov",
        "course_title": "Python & FastAPI Microservices",
        "lesson_title": "1.2 Kinescope DRM Video Integration",
        "submission_text": "Kinescope API key orqali video yuklash moduli sinovdan o'tkazildi.",
        "status": "Approved",
        "grade": 5,
        "feedback": "Ajoyib bajarilgan!",
        "submitted_at": "Kecha, 18:45"
    }
]

@router.get("/", response_model=List[HomeworkSubmission])
async def list_homework_submissions():
    return FAKE_SUBMISSIONS

@router.post("/grade", response_model=HomeworkSubmission)
async def grade_homework(req: GradeRequest):
    for sub in FAKE_SUBMISSIONS:
        if sub["id"] == req.submission_id:
            sub["grade"] = req.grade
            sub["status"] = req.status
            sub["feedback"] = req.feedback
            return sub
    raise HTTPException(status_code=404, detail="Homework submission not found")
