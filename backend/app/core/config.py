"""
Configuration settings for the application.

This module handles configuration settings loaded from environment variables
or configuration files.
"""

import logging
from enum import Enum
from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, Enum):
    """Log level enum."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    """
    Application settings.

    Parameters
    ----------
    API_V1_STR : str
        API version string used in URL paths
    PROJECT_NAME : str
        Name of the project
    DATABASE_URL : str
        Database connection string
    LOG_LEVEL : LogLevel
        Application logging level
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SFAR Antibioprophylaxie API"
    DATABASE_URL: str = Field("sqlite:///./antibioprophylaxie.db", description="Database URL")
    LOG_LEVEL: LogLevel = Field(LogLevel.INFO, description="Logging level")

    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v: str) -> str:
        """
        Validate and normalize database URL.

        Parameters
        ----------
        v : str
            Database URL to validate

        Returns
        -------
        str
            Validated database URL
        """
        return v


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns
    -------
    Settings
        Application settings
    """
    return Settings()


# Configure logging
def setup_logging() -> None:
    """Configure application logging."""
    settings = get_settings()
    
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
