
from fastapi.responses import JSONResponse
from fastapi import Request

class CustomException(Exception):
    def __init__(
            self, message: str | None = None, 
            errors: str | None = None, 
            code: int | None = None
        ):
        self.message = message
        self.errors = errors
        self.code = code


async def custom_exception_handler(request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code if exc.code else 400,
        content={
            "status": "failed",
            "message": exc.message,
            "errors": exc.errors
        }
    )
        

class InvalidEmailException(CustomException):
    pass

class PasswordMismatchException(CustomException):
    pass

class PasswordPolicyViolationException(CustomException):
    pass

class UserNotFoundException(CustomException):
    pass

class AuthenticationFailedException(CustomException):
    pass

class UserAlreadyExistsException(CustomException):
    pass

class UnauthorizedAccessException(CustomException):
    pass