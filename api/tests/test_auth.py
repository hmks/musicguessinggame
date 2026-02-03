from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.core.security import decode_access_token
from app.main import app

client = TestClient(app)

def test_register_and_login_with_username():
    payload = {"username": "testuser", "password": "Passw0rd!"}
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code in {200, 201}
    resp = client.post("/auth/login", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    token = data.get("access_token")
    assert token

    settings = get_settings()
    subject = decode_access_token(token, settings.jwt_secret)
    assert subject == "testuser"
