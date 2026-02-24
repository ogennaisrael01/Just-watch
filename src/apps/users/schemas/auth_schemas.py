from typing import Annotated

from pydantic import (
    BaseModel, 
    field_validator, 
    model_validator, 
    constr, 
)

from asyncio.log import logger

from services import AuthService
from exceptions import (
    InvalidEmailException,
    PasswordMismatchException,
    PasswordPolicyViolationException
)

class RegisterSchema(BaseModel):
    username: Annotated[str, constr(strip_whitespace=True, max_length=50, min_length=3)]
    email: Annotated[str, constr(strip_whitespace=True, max_length=50, min_length=8)]
    first_name: Annotated[str, constr(strip_whitespace=True, max_length=50, min_length=3)] = None
    last_name: Annotated[str, constr(strip_whitespace=True, max_length=50, min_length=4)] = None
    password: Annotated[str, constr(max_length=50, min_length=3)]
    confirm_password: Annotated[str, constr(max_length=5, min_length=3)]

    @field_validator("email")
    @classmethod
    async def validate_email(cls, value: str):
        email = value.strip()
        valid, valid_email = await AuthService.validate_email(email)
        if valid:
            return valid_email
        raise InvalidEmailException("Error validating email address")

    @field_validator("password")
    @classmethod
    async def validate_password(cls, value):
        is_valid = await AuthService.password_validator(value)
        if not is_valid:
            raise PasswordPolicyViolationException("Password invalid")
        return value.strip()
    
    @field_validator("confirm_password")
    @classmethod
    async def validate_confirm_password(cls, value):
        is_valid = await AuthService.password_validator(value)
        if not is_valid:
            raise PasswordPolicyViolationException("Confirm password invalid")
        return value.strip()
    
    @model_validator(mode="after")
    async def password_match(self):
            is_match = await AuthService.passwordmismatch(self.password, self.confirm_password)
            if not is_match:
                 raise PasswordMismatchException("Password mismatch")
            return self