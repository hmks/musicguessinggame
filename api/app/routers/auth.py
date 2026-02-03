from typing import Dict

from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.core.security import create_access_token, hash_password, verify_password
from app.db.mongo import get_db
from app.schemas.auth import AuthLoginRequest, AuthRegisterRequest, MessageResponse, TokenResponse

router = APIRouter()

_in_memory_users: Dict[str, dict] = {}


def _identifier_from_payload(payload: AuthLoginRequest | AuthRegisterRequest) -> str:
    return payload.email or payload.username or ""


def _user_exists(email: str | None, username: str | None) -> bool:
    if email and email in _in_memory_users:
        return True
    if username and username in _in_memory_users:
        return True
    return False


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: AuthRegisterRequest):
    db = get_db()
    hashed = hash_password(payload.password)

    if db is None:
        if _user_exists(payload.email, payload.username):
            raise HTTPException(status_code=400, detail="User already exists")
        user = {"email": payload.email, "username": payload.username, "password": hashed}
        if payload.email:
            _in_memory_users[payload.email] = user
        if payload.username:
            _in_memory_users[payload.username] = user
        return MessageResponse(message="registered (in-memory)")

    users = db["users"]
    query = {"$or": []}
    if payload.email:
        query["$or"].append({"email": payload.email})
    if payload.username:
        query["$or"].append({"username": payload.username})
    if query["$or"] and users.find_one(query):
        raise HTTPException(status_code=400, detail="User already exists")
    users.insert_one({"email": payload.email, "username": payload.username, "password": hashed})
    return MessageResponse(message="registered")


@router.post("/login", response_model=TokenResponse)
async def login(payload: AuthLoginRequest):
    db = get_db()
    identifier = _identifier_from_payload(payload)

    if db is None:
        user = _in_memory_users.get(identifier)
        if not user or not verify_password(payload.password, user.get("password", "")):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        users = db["users"]
        query = {"$or": []}
        if payload.email:
            query["$or"].append({"email": payload.email})
        if payload.username:
            query["$or"].append({"username": payload.username})
        user = users.find_one(query) if query["$or"] else None
        if not user or not verify_password(payload.password, user.get("password", "")):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    settings = get_settings()
    token = create_access_token(identifier, settings.jwt_secret, settings.jwt_expires_min)
    return TokenResponse(access_token=token, token_type="bearer")
