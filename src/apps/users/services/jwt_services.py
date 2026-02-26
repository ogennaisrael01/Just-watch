
import jose
from jose import jwt
from datetime import datetime, timedelta

from src.apps.users.schemas import JWTSchemaResponse
from src.apps.users.exceptions import JWTException

from .security import (
    verify_keys, SECRET_KEY, 
    ALGORITHM, EXPIRES_IN,
    REFRESH_LIFESPAN
)

class JWTService:

    @staticmethod
    async def create_access_token(payload: dict) -> str:
        payload.update({"exp": datetime.now() + timedelta(minutes=EXPIRES_IN)})
        try:
            encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        except jose.JWTError:
            raise ValueError("JWT invalid for access token")
        return encoded_jwt
    
    @staticmethod
    async def create_refresh_token(payload: dict) -> str:
        payload.update({"exp": datetime.now() + timedelta(days=REFRESH_LIFESPAN)})
        try:
            encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        except jose.JWTError:
            raise ValueError("JWT invalid for refresh token")
        return encoded_jwt
    
    @staticmethod
    async def encode_secret_key(payload: dict, expired_in: int | None = None)-> JWTSchemaResponse:
        """ Returns both the access and refresh key """
        tokens = ("refresh_token", "access_token ")
        payload_copy = payload.copy()
        if expired_in is not None:
            exp = datetime.now() + timedelta(minutes=expired_in)
        else:
            exp = datetime.now() + timedelta(minutes=EXPIRES_IN)
        payload_copy.update({"exp": exp})
        token_data = {}
        for token in tokens:
            if token.startswith("refresh"):
                encoded_jwt = await JWTService.create_refresh_token(payload)
                token_data["refresh_token"] = encoded_jwt
            else:
                encoded_jwt = await JWTService.create_access_token(payload)
                token_data["access_token"] = encoded_jwt
        token_response = JWTSchemaResponse(**token_data)
        return token_response
        

    @staticmethod
    async def decode_jwt_token(token: str) -> dict:
        if token is None:
            raise JWTException(
                message="Token not found", errors="Jwt token not found",
                code=404
            )
        try:
            payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        except jose.JWTError as e:
            raise JWTException(
                message="Token Invalid", errors=f"Errors: {str(e)}",
                code=400
            )
        return payload



            
