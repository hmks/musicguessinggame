import random
import re
from typing import Dict, Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.db.mongo import get_db
from app.routers.songs import get_seed_songs
from app.schemas.games import (
    FinishResponse,
    GamesResponse,
    GuessRequest,
    GuessResponse,
    SongPrompt,
    StartGameRequest,
    StartGameResponse,
)

router = APIRouter()

_in_memory_games: Dict[str, dict] = {}


def _normalize_guess(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _song_prompt(song) -> SongPrompt:
    return SongPrompt(
        id=song.id,
        artist=song.artist,
        year=song.year,
        preview_url=song.preview_url,
        source=song.source,
    )


def _load_game(game_id: str) -> Optional[dict]:
    db = get_db()
    if db is None:
        return _in_memory_games.get(game_id)
    return db["games"].find_one({"_id": game_id})


def _save_game(game: dict) -> None:
    db = get_db()
    if db is None:
        _in_memory_games[game["_id"]] = game
        return
    db["games"].replace_one({"_id": game["_id"]}, game, upsert=True)


@router.get("/", response_model=GamesResponse)
async def list_games():
    db = get_db()
    if db is None:
        return GamesResponse(items=list(_in_memory_games.keys()))
    ids = [doc["_id"] for doc in db["games"].find({}, {"_id": 1})]
    return GamesResponse(items=ids)


@router.post("/start", response_model=StartGameResponse)
async def start_game(payload: StartGameRequest):
    songs = get_seed_songs()
    count = max(1, min(payload.count, len(songs)))
    selection = random.sample(songs, count)
    game_id = str(uuid4())

    game = {
        "_id": game_id,
        "song_ids": [song.id for song in selection],
        "current_index": 0,
        "score": 0,
        "correct_count": 0,
        "finished": False,
    }
    _save_game(game)

    return StartGameResponse(
        game_id=game_id,
        round=1,
        total_rounds=len(selection),
        score=0,
        song=_song_prompt(selection[0]),
    )


@router.post("/{game_id}/guess", response_model=GuessResponse)
async def guess_song(game_id: str, payload: GuessRequest):
    game = _load_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.get("finished"):
        raise HTTPException(status_code=400, detail="Game already finished")

    songs = {song.id: song for song in get_seed_songs()}
    song_id = game["song_ids"][game["current_index"]]
    song = songs.get(song_id)
    if not song:
        raise HTTPException(status_code=500, detail="Song not found")

    guess_value = _normalize_guess(payload.guess)
    correct_value = _normalize_guess(song.title)
    correct = guess_value == correct_value

    if correct:
        game["score"] += 1
        game["correct_count"] += 1

    game["current_index"] += 1
    finished = game["current_index"] >= len(game["song_ids"])
    game["finished"] = finished

    next_song = None
    if not finished:
        next_id = game["song_ids"][game["current_index"]]
        next_song = _song_prompt(songs[next_id])

    _save_game(game)

    return GuessResponse(
        correct=correct,
        correct_title=song.title,
        round=min(game["current_index"] + 1, len(game["song_ids"])),
        total_rounds=len(game["song_ids"]),
        score=game["score"],
        finished=finished,
        next_song=next_song,
    )


@router.post("/{game_id}/finish", response_model=FinishResponse)
async def finish_game(game_id: str):
    game = _load_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    game["finished"] = True
    _save_game(game)

    return FinishResponse(
        game_id=game_id,
        total_rounds=len(game["song_ids"]),
        score=game["score"],
        correct_count=game.get("correct_count", 0),
    )
