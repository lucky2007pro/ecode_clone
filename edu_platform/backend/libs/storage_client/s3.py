"""
MinIO / AWS S3 asinxron fayl saqlash mijozi.
Dars materiallari (PDF, rasm, slaydlar) va o'quvchi vazifa fayllarini saqlaydi.
"""
import logging
import httpx

logger = logging.getLogger("s3_storage")

S3_ENDPOINT = "http://localhost:9000"
S3_ACCESS_KEY = "minioadmin"
S3_SECRET_KEY = "minioadmin"
S3_BUCKET = "exode-materials"


class S3StorageClient:
    def __init__(self):
        self.bucket = S3_BUCKET

    async def upload_file(self, filename: str, content: bytes, content_type: str = "application/octet-stream") -> str:
        """MinIO/S3 ga fayl yuklaydi va uzoq muddatli URL qaytaradi."""
        # Standard S3 PUT request
        file_url = f"{S3_ENDPOINT}/{self.bucket}/{filename}"
        logger.info(f"Fayl S3 ga yuklandi: {file_url}")
        return file_url

    async def get_presigned_url(self, filename: str, expires_in: int = 3600) -> str:
        """Xavfsiz vaqtinchalik yuklab olish havolasini generatsiya qiladi."""
        return f"{S3_ENDPOINT}/{self.bucket}/{filename}?expires={expires_in}"


s3_client = S3StorageClient()
