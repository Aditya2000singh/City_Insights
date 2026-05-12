from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # MongoDB
    mongodb_url: str = ""
    mongodb_db_name: str = "city"

    # External APIs
    openweather_api_key: str = ""
    openaq_api_key: str = ""
    exchange_rate_api_key: str = ""

    # App
    app_env: str = "development"
    poll_interval_seconds: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
