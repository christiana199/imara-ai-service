"""
ImaraFund Configuration Management
Environment-based settings with your proven algorithm weights
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """ImaraFund application settings"""

    # Project Information
    PROJECT_NAME: str = "ImaraFund"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered funding matcher for African SMEs"

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./imarafund.db"

    # AI Configuration (Your Gemini 2.5 Flash setup)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Your Proven Matching Algorithm Weights (40/30/20/10)
    GEOGRAPHY_WEIGHT: float = 0.40  # Most important for African SMEs
    SECTOR_WEIGHT: float = 0.30     # Business alignment
    FUNDING_WEIGHT: float = 0.20    # Financial feasibility
    STAGE_WEIGHT: float = 0.10      # Development stage compatibility

    # Security
    SECRET_KEY: str = "imarafund-secret-key-change-in-production"

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()