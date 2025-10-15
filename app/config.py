"""
Configuration module for autocash-ultimate.

Loads settings from environment variables with secure defaults.
Never commits secrets - use GitHub Secrets or vault solutions.
"""

import os
from pathlib import Path
from typing import Optional


class Settings:
    """Application settings loaded from environment variables."""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    TEMPLATES_DIR = BASE_DIR / "templates"
    SITE_OUT_DIR = BASE_DIR / "site-out"
    
    # Application
    APP_NAME = "autocash-ultimate"
    APP_VERSION = "0.1.0"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/autocash.db")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE-ME-IN-PRODUCTION-USE-SECRETS")
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "CHANGE-ME-IN-PRODUCTION")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    
    # Content Generation
    REVIEW_REQUIRED = os.getenv("REVIEW_REQUIRED", "true").lower() == "true"
    MIN_ARTICLE_WORDS = int(os.getenv("MIN_ARTICLE_WORDS", "700"))
    MAX_ARTICLE_WORDS = int(os.getenv("MAX_ARTICLE_WORDS", "1200"))
    
    # Privacy & LGPD
    DATA_RETENTION_DAYS = int(os.getenv("DATA_RETENTION_DAYS", "365"))
    CONSENT_REQUIRED = os.getenv("CONSENT_REQUIRED", "true").lower() == "true"
    IP_SALT = os.getenv("IP_SALT", "CHANGE-ME-RANDOM-SALT-32-CHARS")
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Monitoring
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    
    # Kill switch
    KILL_SWITCH_ENABLED = os.getenv("KILL_SWITCH_ENABLED", "false").lower() == "true"
    
    # External APIs (optional, for future use)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_PORT: Optional[int] = int(os.getenv("SMTP_PORT", "587")) if os.getenv("SMTP_PORT") else None
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    
    @classmethod
    def validate(cls) -> None:
        """Validate critical settings before app startup."""
        if cls.ENVIRONMENT == "production":
            if cls.SECRET_KEY == "CHANGE-ME-IN-PRODUCTION-USE-SECRETS":
                raise ValueError("SECRET_KEY must be set in production")
            if cls.ADMIN_TOKEN == "CHANGE-ME-IN-PRODUCTION":
                raise ValueError("ADMIN_TOKEN must be set in production")
            if cls.IP_SALT == "CHANGE-ME-RANDOM-SALT-32-CHARS":
                raise ValueError("IP_SALT must be set in production")
        
        # Ensure directories exist
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        cls.SITE_OUT_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
