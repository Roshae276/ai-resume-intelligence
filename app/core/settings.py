from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    UPLOAD_FOLDER: str
    
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    DATABASE_URL:str
    QDRANT_URL: str

    QDRANT_COLLECTION: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()