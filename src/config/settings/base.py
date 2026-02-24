from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv
from asyncio.log   import logger
import os

load_dotenv()

class BaseSetting(BaseSettings):
    """ Developerment Setting """   
    DEBUG: bool
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore'
    )