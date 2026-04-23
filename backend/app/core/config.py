from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "北京高校与景区个性化旅游系统"
    api_prefix: str = "/api"
    debug: bool = True
    cors_origins: list[str] = Field(default=["http://localhost:5173", "http://127.0.0.1:5173"])
    storage_backend: str = "postgres"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/travel_system"
    base_dir: Path = Path(__file__).resolve().parents[3]
    dataset_dir: Path = base_dir / "datasets" / "prod"
    model_config = SettingsConfigDict(env_prefix="TRAVEL_", extra="ignore", env_file=".env", env_file_encoding="utf-8")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> str | list[str]:
        if isinstance(value, str):
            text = value.strip()
            # Keep JSON-array style values for pydantic to parse.
            if text.startswith("["):
                return value
            return [item.strip() for item in text.split(",") if item.strip()]
        return value

    @field_validator("storage_backend")
    @classmethod
    def normalize_storage_backend(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"json", "postgres"}:
            raise ValueError("TRAVEL_STORAGE_BACKEND must be either 'json' or 'postgres'")
        return normalized


@lru_cache
def get_settings() -> Settings:
    return Settings()
