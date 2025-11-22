"""Application configuration module."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Custom base settings class."""

    database_url: str

    jwt_secret: str = (
        "3a7e9b2c8d1f0a5b6e4d7c3b9a8f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f"  # noqa: S105
    )
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",  # sem prefixo
        extra="ignore",
    )


settings = Config()  # type: ignore
