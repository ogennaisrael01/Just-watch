from src.config.database.setup import get_db
from helpers import get_user_or_none
from src.apps.users.models.auth_models import User
from src.apps.users.exceptions import UserAlreadyExistsException

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

class UserService:

    @staticmethod
    async def create_user(user_credentials: dict, db: AsyncSession = Depends(get_db)):
        email, username = user_credentials.get("email"), user_credentials.get("username")

        if email is None or username is None:
            raise ValueError("email and username cannot be empty")
        user = await get_user_or_none(email=email, username=username, db=db)
        if user:
            raise UserAlreadyExistsException("User with email or username already exists")
        new_user = User(**user_credentials)
        await db.add(new_user)
        await db.commit()
        await db.refresh()

        return new_user 
