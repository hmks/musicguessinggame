from fastapi import APIRouter

from app.db.mongo import get_db

router = APIRouter()

@router.get("/health")
async def health_check():
    db = get_db()
    status = "ok" if db is not None else "degraded"
    return {"status": status, "service": "api"}
