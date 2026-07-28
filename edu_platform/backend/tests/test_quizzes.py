"""
Quizzes: javob sizishi (leak) va serverda baholash testlari.
"""
import pytest
from httpx import AsyncClient


async def _create_quiz_with_question(client: AsyncClient, admin_auth):
    """Kurs -> dars -> test -> savol zanjirini yaratadi."""
    headers = admin_auth["headers"]
    course = await client.post("/api/v1/courses/", json={
        "title": "Quiz Course", "slug": "quiz-course",
        "description": "Quiz testlar uchun kurs", "price": 1000.0,
    }, headers=headers)
    assert course.status_code == 201

    lesson = await client.post("/api/v1/lessons/", json={
        "course_id": course.json()["id"], "title": "Dars 1", "lesson_type": "video", "order": 0,
    }, headers=headers)
    assert lesson.status_code == 201

    quiz = await client.post("/api/v1/quizzes/", json={
        "lesson_id": lesson.json()["id"], "title": "Test 1", "passing_score": 50,
    }, headers=headers)
    assert quiz.status_code == 201

    question = await client.post(f"/api/v1/quizzes/{quiz.json()['id']}/questions", json={
        "text": "2 + 2 = ?", "order": 0,
        "answers": [
            {"text": "4", "is_correct": True},
            {"text": "5", "is_correct": False},
        ],
    }, headers=headers)
    assert question.status_code == 201
    return quiz.json()["id"]


@pytest.mark.asyncio
async def test_take_quiz_hides_is_correct(client: AsyncClient, admin_auth):
    """/take endpoint javob variantlarida is_correct'ni sizdirmasligi kerak."""
    quiz_id = await _create_quiz_with_question(client, admin_auth)
    res = await client.get(f"/api/v1/quizzes/{quiz_id}/take", headers=admin_auth["headers"])
    assert res.status_code == 200
    questions = res.json()
    assert len(questions) == 1
    assert len(questions[0]["answers"]) == 2
    for answer in questions[0]["answers"]:
        assert "is_correct" not in answer


@pytest.mark.asyncio
async def test_submit_quiz_grades_server_side(client: AsyncClient, admin_auth):
    """To'g'ri va noto'g'ri javoblar serverda baholanib, natija saqlanadi."""
    quiz_id = await _create_quiz_with_question(client, admin_auth)
    headers = admin_auth["headers"]

    take = await client.get(f"/api/v1/quizzes/{quiz_id}/take", headers=headers)
    question = take.json()[0]
    correct_id = question["answers"][0]["id"]
    wrong_id = question["answers"][1]["id"]

    res = await client.post(f"/api/v1/quizzes/{quiz_id}/submit", json={
        "answers": {question["id"]: correct_id},
    }, headers=headers)
    assert res.status_code == 200
    assert res.json() == {"score": 1, "total": 1, "percent": 100}

    res = await client.post(f"/api/v1/quizzes/{quiz_id}/submit", json={
        "answers": {question["id"]: wrong_id},
    }, headers=headers)
    assert res.status_code == 200
    assert res.json() == {"score": 0, "total": 1, "percent": 0}

    results = await client.get("/api/v1/quizzes/results/my", headers=headers)
    assert results.status_code == 200
    data = results.json()
    assert len(data) == 2
    assert data[0]["score"] == 0  # eng so'nggi natija birinchi keladi
    assert all(r["quiz_id"] == quiz_id for r in data)


@pytest.mark.asyncio
async def test_take_quiz_other_school_returns_404(client: AsyncClient, admin_auth):
    """Boshqa maktab testi linchga ko'rinmasligi kerak."""
    random_id = "00000000-0000-0000-0000-000000000001"
    res = await client.get(f"/api/v1/quizzes/{random_id}/take", headers=admin_auth["headers"])
    assert res.status_code == 404
