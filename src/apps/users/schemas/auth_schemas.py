from typing import Annotated
import uuid

from pydantic import (
    BaseModel, 
    field_validator, 
    model_validator, 
    constr, 
)

from asyncio.log import logger

from .auth_validator import AuthService

from src.apps.users.exceptions import (
    InvalidEmailException,
    PasswordMismatchException,
    PasswordPolicyViolationException
)

class BaseAuthClass(BaseModel):
    email: Annotated[str, constr(strip_whitespace=True, max_length=50, min_length=8)]
    password: Annotated[str, constr(max_length=50, min_length=3)]

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        email = value.strip()
        valid, valid_email = AuthService.validate_email(email)
        if valid:
            return valid_email
        raise InvalidEmailException(
            message="Error validating email address", 
            errors=f"Invalid email address: {email}", code=400)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        is_valid = AuthService.password_validator(value)
        if not is_valid["valid"]:
            raise PasswordPolicyViolationException(
                message="Password does not meet policy requirements",
                errors=str(is_valid["message"]))
        return value.strip()

class RegisterSchema(BaseAuthClass):
    username: Annotated[str, constr(strip_whitespace=True, max_length=50, min_length=3)]
    first_name: Annotated[str, constr(strip_whitespace=True, max_length=50, min_length=3)] = None
    last_name: Annotated[str, constr(strip_whitespace=True, max_length=50, min_length=4)] = None
    confirm_password: Annotated[str, constr(max_length=5, min_length=3)]

    
    
    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, value):
        is_valid = AuthService.password_validator(value)
        if not is_valid["valid"]:
            raise PasswordPolicyViolationException(
                message="Password does not meet policy requirements",
                errors=str(is_valid["message"]))
        return value.strip()
    
    @model_validator(mode="after")
    def password_match(self):
            is_match = AuthService.passwordmismatch(self.password, self.confirm_password)
            if not is_match:
                 raise PasswordMismatchException(
                    message="Password mismatch",
                    errors="The password and confirm password fields do not match"
                 )
            return self

class LogInSchema(BaseAuthClass):
    pass

class BaseResponse(BaseModel):
    status: str | None = None
    message: str | None = None
    code: int | None = None

class JWTSchemaResponse(BaseResponse):
    token_type: str | None = "Bearer"
    access_token: str
    refresh_token: str

class RegistrationResponse(BaseResponse):
    pass

class UserProfileResponse(BaseModel):
    user_id: uuid.UUID
    email: str
    first_name: str
    updated_at: str
    username: str
    last_name: str
    created_at: str