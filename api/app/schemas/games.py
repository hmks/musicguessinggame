from typing import List

from pydantic import BaseModel

class Game(BaseModel):
    id: str | None = None
    status: str | None = None

class GamesResponse(BaseModel):
    items: List[Game]
