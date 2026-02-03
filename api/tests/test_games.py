from fastapi.testclient import TestClient

from app.main import app
from app.routers.songs import get_seed_songs

client = TestClient(app)

def test_start_and_guess_game():
    start_resp = client.post("/games/start", json={"count": 2})
    assert start_resp.status_code == 200
    start_data = start_resp.json()
    game_id = start_data["game_id"]
    assert start_data["song"]["id"]

    songs = {song.id: song for song in get_seed_songs()}
    first_song = songs[start_data["song"]["id"]]

    guess_resp = client.post(f"/games/{game_id}/guess", json={"guess": first_song.title})
    assert guess_resp.status_code == 200
    guess_data = guess_resp.json()
    assert guess_data["score"] >= 1
