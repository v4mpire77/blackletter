from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings following Context Engineering Framework"""
    
    # App Configuration
    APP_NAME: str = "Blackletter Systems API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Database Configuration (Supabase Cloud)
    DATABASE_URL: str
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    
    # Redis/Celery Configuration
    REDIS_URL: str = "redis://localhost:6379"
    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"
    
    # LLM Configuration
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4"
    LLM_MAX_TOKENS: int = 4000
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".docx", ".txt"]
    UPLOAD_DIR: str = "uploads"
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Security Configuration
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def validate_required_settings(self) -> bool:
        """Validate required settings for Context Engineering Framework compliance"""
        required_fields = [
            'DATABASE_URL', 'SECRET_KEY', 'REDIS_URL'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(self, field, None):
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"Missing required settings: {', '.join(missing_fields)}")
        
        return True

# Global settings instance
settings = Settings()

# Validate on import
settings.validate_required_settings()