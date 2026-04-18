from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "北京高校与景区个性化旅游系统"
    api_prefix: str = "/api"
    debug: bool = True
    cors_origins: list[str] = Field(default=["http://localhost:5173"])
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/travel_system"
    base_dir: Path = Path(__file__).resolve().parents[3]
    dataset_dir: Path = base_dir / "datasets" / "prod"
    model_config = SettingsConfigDict(env_prefix="TRAVEL_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
