# Exode Platform — Modular FastAPI Architecture

Clean, modular, domain-driven design structure:

`
fast_async/
├── users/          # Users & Auth (auth.py, crud.py, models.py, router.py, schema.py)
├── schools/        # School management (crud.py, models.py, router.py, schema.py)
├── courses/        # Course & Homework (crud.py, models.py, router.py, schema.py)
├── videos/         # Kinescope API (kinescope.py, models.py, router.py, schema.py)
├── crm/            # Kommo CRM (kommo.py, models.py, router.py, schema.py)
├── payments/       # Payments (payme.py, click.py, uzum.py, crud.py, models.py, router.py, schema.py)
├── notifications/ # Notifications (telegram.py, sms.py, email.py, router.py)
├── tests/          # Tests (conftest.py, test_users.py, test_courses.py, test_payments.py)
├── db.py
├── redis_client.py
├── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
`
