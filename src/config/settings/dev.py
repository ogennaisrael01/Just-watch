from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv
from asyncio.log   import logger

load_dotenv()

class DevelopmentSetting(BaseSettings):
    """ Developerment Setting """ 

    DATABASE_URL: str  = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore'
    )