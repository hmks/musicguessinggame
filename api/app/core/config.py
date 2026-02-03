import os
from functools import lru_cache

class Settings:
    def __init__(self) -> None:
        self.api_port = int(os.getenv("API_PORT", "8001"))
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.mongo_db = os.getenv("MONGO_DB", "musiguess")
        self.jwt_secret = os.getenv("JWT_SECRET", "change-me")
        self.jwt_expires_min = int(os.getenv("JWT_EXPIRES_MIN", "43200"))
        cors = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:19006")
        self.cors_origins = [origin.strip() for origin in cors.split(",") if origin.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
