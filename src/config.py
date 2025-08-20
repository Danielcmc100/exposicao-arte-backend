# Copyright 2025 PSTG-Tech
# All rights reserved.

"""Application configuration module."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Custom base settings class."""

    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Config()  # type: ignore
