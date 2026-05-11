"""
Configuration management for Nexus AI OS
"""
from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List, Union, Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Nexus AI Operating System"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "change-this-in-production"
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database
    DATABASE_URL: str = "postgresql://nexus:nexus_secure_password@localhost:5432/nexus"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_MAX_CONNECTIONS: int = 50
    
    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "nexus_graph_password"
    
    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "nexus_embeddings"
    EMBEDDING_DIMENSION: int = 768
    
    # Google AI
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL_PRO: str = "gemini-1.5-pro-latest"
    GEMINI_MODEL_FLASH: str = "gemini-1.5-flash-latest"
    MAX_TOKENS: int = 8192
    TEMPERATURE: float = 0.7
    
    # Agent Configuration
    MAX_AGENTS: int = 50
    AGENT_TIMEOUT: int = 300
    MAX_TASK_RETRIES: int = 3
    AGENT_HEARTBEAT_INTERVAL: int = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # Performance
    WORKER_CONCURRENCY: int = 4
    MAX_OVERFLOW: int = 10
    POOL_SIZE: int = 20
    POOL_RECYCLE: int = 3600
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings

# Made with Bob
