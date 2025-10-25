from pydantic import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_service_key: str
    openai_api_key: str
    anthropic_api_key: str
    qdrant_url: str
    qdrant_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()