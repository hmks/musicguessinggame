from typing import List

from pydantic import BaseModel

class Song(BaseModel):
    id: str | None = None
    title: str | None = None
    artist: str | None = None

class SongsResponse(BaseModel):
    items: List[Song]
