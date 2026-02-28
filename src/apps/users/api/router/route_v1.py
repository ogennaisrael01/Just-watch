from fastapi import (
    APIRouter, Depends, 
    status, HTTPException, 
    Request
)
from fastapi.encoders import jsonable_encoder
from fastapi_cache.decorator import cache

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.users.schemas import (
    RegistrationResponse, 
    RegisterSchema, LogInSchema,
    UserProfileResponse
)
from src.apps.users.helpers import hash_password
from src.apps.users.services import  UserService
from src.config.database.setup import get_db
from src.apps.users.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException
)
from src.apps.users.models.auth_models import User
from src.manage import limiter

router = APIRouter(tags=["Auth"], prefix="/v1/auth")



@router.post("/register/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register_user(request: Request, data: RegisterSchema, db: AsyncSession = Depends(get_db)):
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

@router.post("/login/", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def login_user(request: Request, login_data: LogInSchema, db: AsyncSession = Depends(get_db)):
    credentials = login_data.model_dump()
    try:
        authenticate_user = await UserService.authenticate_user(user_credentials=credentials, db=db)
    except UserNotFoundException as e:
        raise e
    jsonable_encoder(authenticate_user)
    return authenticate_user

@router.get("/user-me/", status_code=status.HTTP_200_OK, response_model=None)
@cache(expire=60 * 10)
async def user_profile(
    current_user: User = Depends(UserService.get_current_user),
    db: AsyncSession = Depends(get_db)
):

    try:
        user_profile = await UserService.get_current_user_profile(
            current_user=current_user,
            db=db
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    if current_user == 0:
        result = current_user
    else:
        result = jsonable_encoder(user_profile)
    
    return {
        "status": "success",
        "result": UserProfileResponse(**result)
    }

    