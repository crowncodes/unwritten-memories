"""
Application settings using Pydantic.
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application settings
    app_name: str = "Unwritten"
    debug: bool = False
    log_level: str = "INFO"
    
    # API Keys (optional)
    wandb_api_key: Optional[str] = Field(None, alias="WANDB_API_KEY")
    hf_token: Optional[str] = Field(None, alias="HF_TOKEN")
    
    # Paths
    data_dir: str = "data"
    models_dir: str = "models"
    logs_dir: str = "logs"


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get or create the global settings instance.
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

