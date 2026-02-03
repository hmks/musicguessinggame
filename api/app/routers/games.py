from fastapi import APIRouter

from app.schemas.games import GamesResponse

router = APIRouter()

@router.get("/", response_model=GamesResponse)
async def list_games():
    return GamesResponse(items=[])
