"""
API Gateway proksi yo'naltirish mantig'i.
Barcha kelayotgan request'larni tegishli mikroservislarga httpx orqali forwarding qiladi.
"""
from fastapi import APIRouter, Request, Response
import httpx

from app.core.config import settings

router = APIRouter()

client = httpx.AsyncClient(timeout=30.0)


async def proxy_request(request: Request, target_url: str) -> Response:
    """Kelgan HTTP requestni nishon servisga proksi qiladi."""
    body = await request.body()
    headers = dict(request.headers)
    # Host header'ini almashtiramiz
    headers.pop("host", None)

    response = await client.request(
        method=request.method,
        url=target_url,
        headers=headers,
        content=body,
        params=request.query_params,
    )
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


# --- AUTH SERVICE PROXY ---
@router.api_route("/api/v1/auth/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def auth_proxy(request: Request, path: str):
    target_url = f"{settings.AUTH_SERVICE_URL}/api/v1/auth/{path}"
    return await proxy_request(request, target_url)


@router.api_route("/api/v1/users/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def users_proxy(request: Request, path: str):
    target_url = f"{settings.AUTH_SERVICE_URL}/api/v1/users/{path}"
    return await proxy_request(request, target_url)


# --- SCHOOL SERVICE PROXY ---
@router.api_route("/api/v1/schools/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def schools_proxy(request: Request, path: str):
    target_url = f"{settings.SCHOOL_SERVICE_URL}/api/v1/schools/{path}"
    return await proxy_request(request, target_url)


# --- COURSE SERVICE PROXY ---
@router.api_route("/api/v1/courses/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def courses_proxy(request: Request, path: str):
    target_url = f"{settings.COURSE_SERVICE_URL}/api/v1/courses/{path}"
    return await proxy_request(request, target_url)
