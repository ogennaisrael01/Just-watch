from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv
from asyncio.log import logger

load_dotenv()

class ProdSettings(BaseSettings):
    """Production settings."""
    DATABASE_URL:str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore'
    )