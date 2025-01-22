from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "GitHub RAG API"
    GITHUB_TOKEN: str
    OPENAI_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()

