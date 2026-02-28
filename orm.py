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

    url = "https://api.themoviedb.org/3/"
    api_key = "a0d130f1658b6b75480aac43e2d52021"

    response = requests.get(url=url + "discover/movie", params={'with_genres': "18,878,12,28,9648", 'sort_by': 'popularity.desc', 'api_key': 'a0d130f1658b6b75480aac43e2d52021'})

    response.raise_for_status()
    print(response.json())

       
if __name__ == "__main__":
    asyncio.run(run())
