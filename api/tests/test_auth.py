from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_register_and_login():
    payload = {"email": "test@example.com", "password": "Passw0rd!"}
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code in {200, 201}
    resp = client.post("/auth/login", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
