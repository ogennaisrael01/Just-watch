from src.config.database.setup import AsyncSessionLocal
from src.apps.users.models.auth_models import User

from sqlalchemy import delete

import asyncio
import requests



async def run():
    # async with AsyncSessionLocal() as db:
    #     stmt = delete(User).where(User.email=="ogennaisrael@gmail.com")
    #     user = await db.execute(stmt)
    #     await db.commit()

    # await db.close()

    url = "https://api.themoviedb.org/3"
    api_key = "a0d130f1658b6b75480aac43e2d52021"

    response = requests.get(url=url + "/movie/58437", params={"api_key": api_key})

    response.raise_for_status()
    print(response.json())

       
if __name__ == "__main__":
    asyncio.run(run())
