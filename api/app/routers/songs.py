import json
from functools import lru_cache
from pathlib import Path
from typing import List

from fastapi import APIRouter, Query

from app.schemas.songs import Song, SongsResponse

router = APIRouter()

@lru_cache(maxsize=1)
def get_seed_songs() -> List[Song]:
    seed_path = Path(__file__).resolve().parents[1] / "data" / "songs.json"
    raw = json.loads(seed_path.read_text(encoding="utf-8"))
    return [Song(**item) for item in raw]

@router.get("/", response_model=SongsResponse)
async def list_songs(q: str | None = Query(default=None, min_length=1)):
    songs = get_seed_songs()
    if q:
        query = q.lower()
        songs = [song for song in songs if query in song.title.lower() or query in song.artist.lower()]
    return SongsResponse(items=songs)
