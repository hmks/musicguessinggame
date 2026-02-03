from fastapi import APIRouter

from app.schemas.songs import SongsResponse

router = APIRouter()

@router.get("/", response_model=SongsResponse)
async def list_songs():
    return SongsResponse(items=[])
