from typing import List

from pydantic import BaseModel

class Song(BaseModel):
    id: str
    title: str
    artist: str
    year: int | None = None
    preview_url: str | None = None
    source: str

class SongsResponse(BaseModel):
    items: List[Song]
