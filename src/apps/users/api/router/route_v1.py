from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.users.schemas import (
    RegistrationResponse, 
    RegisterSchema, LogInSchema
)
from src.apps.users.helpers import hash_password
from src.apps.users.services import  UserService, JWTService
from src.config.database.setup import get_db
from src.apps.users.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException
)

router = APIRouter(tags=["Auth"], prefix="/v1/auth")



@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(data: RegisterSchema, db: AsyncSession = Depends(get_db)):
    credentials = data.model_dump()
    password = credentials.get("password")
    credentials["password"] = await hash_password(password)
    credentials.pop("confirm_password")
    try:
        user = await UserService.create_user(credentials, db)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail=f"User found. Try logging in with this provided email or username")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Error creating user: {str(e)}")
    else:
        registration_success = RegistrationResponse(
            status="success",
            message="Registration succeded with no errors.",
            code=201
        )

    if registration_success.status == "success":
        auth_credentials = {"email": user.email, "password": password}
        authenticate_user = await UserService.authenticate_user(user_credentials=auth_credentials, db=db)
        jsonable_encoder(authenticate_user)
    jsonable_encoder(registration_success)
    
    return {
        "registration_response": registration_success,
        "jwt_response": authenticate_user
    }

@router.post("/login/", status=status.HTTP_200_OK)
async def login_user(login_data: LogInSchema, db: AsyncSession = Depends(get_db)):
    credentials = login_data.model_dump()
    try:
        authenticate_user = await UserService.authenticate_user(user_credentials=credentials, db=db)
    except UserNotFoundException as e:
        raise e
    jsonable_encoder(authenticate_user)
    return authenticate_user

    