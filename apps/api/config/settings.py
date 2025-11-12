"""Application settings using Pydantic"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation"""

    # API Configuration
    app_name: str = "Boltflow API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379"

    # OpenAI
    openai_api_key: str

    # JWT Authentication
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # Logging
    log_level: str = "INFO"

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds

    # Scraping
    max_pages_limit: int = 100
    scrape_timeout: int = 300  # seconds

    # AI
    ai_temperature: float = 0.1
    ai_max_tokens: int = 4000
    embedding_cache_ttl: int = 3600  # 1 hour

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    print("Required environment variables: DATABASE_URL, OPENAI_API_KEY")
    raise
