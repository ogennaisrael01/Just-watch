from fastapi import Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config.database.setup import get_db
from  src.apps.users.models.auth_models import User
from src.apps.users.helpers import verify_hashed_password

from uuid import UUID
from functools import lru_cache


@lru_cache()
async def get_user_or_none(
        email: str | None = None, username: str | None = None, 
        pk: UUID | None = None, db: AsyncSession = Depends(get_db)
    ) ->  tuple[bool, User | None]:

    query = await db.execute(select(User).where(
        (User.email == email) | (User.username == username) | (User.user_id == pk)
        ))
    user = query.scalar_one_or_none()
    if user is None:
        return False, None
    return True, user


@lru_cache()
async def authenticate_user(
        email: str, password: str,
        db: AsyncSession = Depends(get_db)
):
    stmt = select(User).where(User.email==email)
    query = await db.execute(stmt)
    user = query.scalar_one()
    hashed_password = user.password
    is_valid_password = await verify_hashed_password(password, hashed_password)
    if is_valid_password:
        return user
    return False
