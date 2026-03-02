import asyncio

from src.config.settings import base_setting

from asyncio.log import logger

import functools

max_retries = 5

SECRET_KEY = getattr(base_setting, "SECRET_KEY")
ALGORITHM = getattr(base_setting, "ALGORITHM")
EXPIRES_IN = getattr(base_setting, "EXPIRES_IN")
REFRESH_LIFESPAN = getattr(base_setting, "REFRESH_LIFESPAN")

async def verify_keys():
    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY is not set in the configuration.")
    if ALGORITHM is None:
        raise ValueError("ALGORITHM is not set in the configuration.")
    if EXPIRES_IN is None:
        raise ValueError("EXPIRES_IN is not set in the configuration.")
    if REFRESH_LIFESPAN is None:
        raise ValueError("REFRESH_LIFESPAN is not set in the configuration.")
    

def retry_on_failure(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):

        for i in range(1, int(max_retries)):
            try:
                result = await func(self, *args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Attempt {i} failed with error: {e}")
                await asyncio.sleep(2)  

                if i > max_retries:
                    raise  ValueError(f"Max Attempts Exceeded, Error: {e}")
    return wrapper