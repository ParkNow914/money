"""
Configuration management for AutoCash Ultimate.
Loads settings from environment variables with validation.
"""
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = Field(default="AutoCash Ultimate")
    app_version: str = Field(default="0.1.0")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    # Security
    secret_key: str = Field(min_length=32)
    encryption_key: str = Field(min_length=32)
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)

    # Database
    database_url: str = Field(default="sqlite:///./data/autocash.db")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")

    # MeiliSearch
    meili_host: str = Field(default="http://localhost:7700")
    meili_master_key: Optional[str] = Field(default=None)

    # Chroma Vector DB
    chroma_host: str = Field(default="localhost")
    chroma_port: int = Field(default=8000)
    chroma_persist_dir: str = Field(default="./chroma_data")

    # Content Generation
    review_required: bool = Field(default=True)
    min_word_count: int = Field(default=700, ge=500)
    max_word_count: int = Field(default=1200, le=3000)
    similarity_threshold: float = Field(default=0.85, ge=0.0, le=1.0)
    generation_batch_size: int = Field(default=5, ge=1, le=50)

    # OpenAI (optional)
    openai_api_key: Optional[str] = Field(default=None)
    openai_model: str = Field(default="gpt-3.5-turbo")

    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60)
    rate_limit_per_hour: int = Field(default=1000)

    # Kill-Switch
    killswitch_file: str = Field(default="/tmp/killswitch.lock")
    killswitch_enabled: bool = Field(default=True)

    # Data Retention
    data_retention_days: int = Field(default=365, ge=30)
    log_retention_days: int = Field(default=90, ge=7)

    # Email (optional)
    smtp_host: Optional[str] = Field(default=None)
    smtp_port: int = Field(default=587)
    smtp_user: Optional[str] = Field(default=None)
    smtp_password: Optional[str] = Field(default=None)
    email_from: str = Field(default="noreply@autocash.local")

    # Analytics
    matomo_url: Optional[str] = Field(default=None)
    matomo_site_id: Optional[str] = Field(default=None)
    matomo_auth_token: Optional[str] = Field(default=None)

    # Prometheus
    prometheus_enabled: bool = Field(default=True)
    metrics_port: int = Field(default=9090)

    # Cloudflare
    cloudflare_api_token: Optional[str] = Field(default=None)
    cloudflare_zone_id: Optional[str] = Field(default=None)
    cloudflare_account_id: Optional[str] = Field(default=None)

    # Oracle Cloud
    oracle_tenancy_id: Optional[str] = Field(default=None)
    oracle_user_id: Optional[str] = Field(default=None)
    oracle_fingerprint: Optional[str] = Field(default=None)
    oracle_region: Optional[str] = Field(default=None)

    # Admin
    admin_username: str = Field(default="admin")
    admin_password_hash: Optional[str] = Field(default=None)
    admin_2fa_enabled: bool = Field(default=False)

    # Feature Flags
    enable_personalization: bool = Field(default=False)
    enable_ab_testing: bool = Field(default=False)
    enable_pod_generation: bool = Field(default=False)

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in allowed:
            raise ValueError(f"Log level must be one of {allowed}")
        return v_upper

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"

    @property
    def database_path(self) -> Optional[Path]:
        """Get database file path for SQLite."""
        if self.database_url.startswith("sqlite"):
            db_path = self.database_url.replace("sqlite:///", "")
            return Path(db_path)
        return None

    def ensure_directories(self) -> None:
        """Ensure required directories exist."""
        dirs = [
            "data",
            "logs",
            "storage",
            "chroma_data",
            "examples",
        ]
        for dir_name in dirs:
            Path(dir_name).mkdir(parents=True, exist_ok=True)

        # Ensure database directory exists
        if self.database_path:
            self.database_path.parent.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to create singleton.
    """
    settings = Settings()
    settings.ensure_directories()
    return settings


# Export singleton instance
settings = get_settings()
