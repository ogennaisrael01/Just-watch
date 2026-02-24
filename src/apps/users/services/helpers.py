from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database.setup import get_db
from  src.apps.users.models.auth_models import User


async def get_user_or_none(
        email: str, username: str, 
        db: AsyncSession = Depends(get_db)
    ):

    user = await db.query(User).filter(
        (User.email == email) | (User.username == username)
    )
    exists = user.scalar().first()
    return exists if exists else None