# Exode Platform — Modular FastAPI Architecture

Clean, modular, domain-driven design structure:

`
fast_async/
├── users/          # Users & Auth (auth.py, crud.py, models.py, router.py, schema.py)
├── schools/        # School management (crud.py, models.py, router.py, schema.py)
├── courses/        # Course & Homework (crud.py, models.py, router.py, schema.py)
├── videos/         # Kinescope API (kinescope.py, models.py, router.py, schema.py)
├── crm/            # Kommo CRM (kommo.py, models.py, router.py, schema.py)
├── payments/       # Payments (coming soon stub: models.py, router.py)
├── notifications/ # Notifications (telegram.py, email.py, router.py)
├── tests/          # Tests (conftest.py, test_users.py, test_courses.py, test_payments.py)
├── db.py
├── redis_client.py
├── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
`

## Migratsiyalar (Alembic)

Baza sxemasi Alembic orqali boshqariladi. Eski `migrations/*.sql` fayllari endi ishlatilmaydi (superseded).

O'rnatish:

```bash
pip install -r requirements.txt
```

Mavjud bazani so'nggi holatga keltirish (`DATABASE_URL` environment o'zgaruvchisi sozlangan bo'lishi kerak):

```bash
alembic upgrade head
```

Agar baza allaqachon mavjud bo'lib, joriy sxema `alembic` tarixsiz yaratilgan bo'lsa, bir marta belgilab qo'ying:

```bash
alembic stamp head
```

Yangi migratsiya yaratish (modellar o'zgarganda):

```bash
alembic revision --autogenerate -m "o'zgarish tavsifi"
```
