from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_videos():
    return [{"id": "v1", "kinescope_id": "kinescope-101"}]
