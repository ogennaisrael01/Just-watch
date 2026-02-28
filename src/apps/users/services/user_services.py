from src.config.database.setup import get_db
from .helpers import get_user_or_none, authenticate_user
from src.apps.users.models.auth_models import User
from src.apps.users.exceptions import (
    UserAlreadyExistsException, 
    UserNotFoundException,
    JWTException
)
from .jwt_services import JWTService

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

bearer_token = OAuth2PasswordBearer(tokenUrl="/login")

class UserService:

    @staticmethod
    async def create_user(user_credentials: dict, db: AsyncSession = Depends(get_db)):
        email, username = user_credentials.get("email"), user_credentials.get("username")

        if email is None or username is None:
            raise ValueError("email and username cannot be empty")
        found, _ = await get_user_or_none(email=email, username=username, db=db)
        if found:
            raise UserAlreadyExistsException(
                message="User already exists with the provided email or username",
                code=400
            )
        new_user = User(**user_credentials)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user 

    @staticmethod
    async def authenticate_user(user_credentials: dict, db: AsyncSession = Depends(get_db)):
        email, password = user_credentials.get("email"), user_credentials.get("password")
        if email is None or password is None:
            raise ValueError("password and email are required for login")
        
        user = await authenticate_user(email=email, password=password, db=db)
        if not user:
            raise UserNotFoundException(
                message="Provided credentials are invalid",
                errors="Invalid request",
                code=404
            )
        user_id = str(user.user_id)
        email = user.email
        payload = {"sub": user_id, "email": email}
        try:
            encoded_secret = await JWTService.encode_secret_key(payload)
        except Exception as e:
            encoded_secret.message = f"Error creating JWT {e}"
            encoded_secret.code = 400
            encoded_secret.status = "failed"
            raise e
        else:
            encoded_secret.message = f"Jwt Created Successfully"
            encoded_secret.code = 200
            encoded_secret.status = "success"
        return encoded_secret
    
    @staticmethod
    async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(bearer_token)):

        payload = await JWTService.decode_jwt_token(token=token)

        sub, email  = payload.get("sub") , payload.get("email")
        if sub is None or email is None:
            raise JWTException(
                message="Payload not found", errors="pk and email are required for successful authorization",
                code=400
            )
        is_valid, user = await get_user_or_none(email=email, pk=sub, db=db)
        if not is_valid:
            raise UserNotFoundException(
                message="User not found", errors="User not found with the provided credentials",
                code=404
            )
        return user

    @staticmethod
    async def get_current_user_profile(current_user, db: AsyncSession = Depends(get_db)):
        found, user = await get_user_or_none(email=current_user.email, pk=current_user.user_id, db=db)

        if not found:
            return 0
        return user