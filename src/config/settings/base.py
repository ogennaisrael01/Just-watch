from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv
from asyncio.log   import logger
import os

load_dotenv()

class BaseSetting(BaseSettings):
    """ Developerment Setting """   
    DEBUG: bool
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRES_IN: int
    REFRESH_LIFESPAN: int
    TMDB_API_KEY: str
    BASE_URL: str
    GEMINI_MODEL: str
    GEMINI_API_KEY: str


    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore'
    )