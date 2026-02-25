from src.config.database.setup import AsyncSessionLocal
from src.apps.users.models.auth_models import User

from sqlalchemy import delete

import asyncio



async def run():
    async with AsyncSessionLocal() as db:
        stmt = delete(User).where(User.email=="ogennaisrael@gmail.com")
        user = await db.execute(stmt)
        await db.commit()

    await db.close()
       
if __name__ == "__main__":
    asyncio.run(run())
