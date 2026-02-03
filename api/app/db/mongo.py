from functools import lru_cache
from typing import Optional

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.core.config import get_settings

@lru_cache
def get_client() -> MongoClient:
    settings = get_settings()
    return MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=2000)


def get_db() -> Optional[object]:
    settings = get_settings()
    try:
        client = get_client()
        client.admin.command("ping")
        return client[settings.mongo_db]
    except PyMongoError:
        return None
