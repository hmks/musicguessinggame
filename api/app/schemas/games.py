from typing import List

from pydantic import BaseModel

class SongPrompt(BaseModel):
    id: str
    artist: str
    year: int | None = None
    preview_url: str | None = None
    source: str

class StartGameRequest(BaseModel):
    count: int = 3

class StartGameResponse(BaseModel):
    game_id: str
    round: int
    total_rounds: int
    score: int
    song: SongPrompt

class GuessRequest(BaseModel):
    guess: str

class GuessResponse(BaseModel):
    correct: bool
    correct_title: str
    round: int
    total_rounds: int
    score: int
    finished: bool
    next_song: SongPrompt | None = None

class FinishResponse(BaseModel):
    game_id: str
    total_rounds: int
    score: int
    correct_count: int

class GamesResponse(BaseModel):
    items: List[str]
