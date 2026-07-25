FROM python:3.11-slim

WORKDIR /app

# Atrof-muhit o'zgaruvchilari
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Sistemaviy paketlar
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt-get/lists/*

# Libs papkasini va servis kodlarini nusxalash
COPY libs /app/libs
COPY services /app/services

# Har bir servis o'z katalogidan ishga tushadi
WORKDIR /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]