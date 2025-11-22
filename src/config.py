"""Application configuration module."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Custom base settings class."""

    database_url: str

    jwt_secret: str = "dev_only_change_me"  # sobrescrito pelo .env em produção
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",  # sem prefixo
        extra="ignore",
    )


settings = Config()  # type: ignore
