from typing import Dict

from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.core.security import create_access_token, hash_password, verify_password
from app.db.mongo import get_db
from app.schemas.auth import AuthLoginRequest, AuthRegisterRequest, MessageResponse, TokenResponse

router = APIRouter()

_in_memory_users: Dict[str, str] = {}

@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: AuthRegisterRequest):
    db = get_db()
    hashed = hash_password(payload.password)

    if db is None:
        if payload.email in _in_memory_users:
            raise HTTPException(status_code=400, detail="User already exists")
        _in_memory_users[payload.email] = hashed
        return MessageResponse(message="registered (in-memory)")

    users = db["users"]
    if users.find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="User already exists")
    users.insert_one({"email": payload.email, "password": hashed})
    return MessageResponse(message="registered")

@router.post("/login", response_model=TokenResponse)
async def login(payload: AuthLoginRequest):
    db = get_db()

    if db is None:
        hashed = _in_memory_users.get(payload.email)
        if not hashed or not verify_password(payload.password, hashed):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        users = db["users"]
        user = users.find_one({"email": payload.email})
        if not user or not verify_password(payload.password, user.get("password", "")):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    settings = get_settings()
    token = create_access_token(payload.email, settings.jwt_secret, settings.jwt_expires_min)
    return TokenResponse(access_token=token, token_type="bearer")
