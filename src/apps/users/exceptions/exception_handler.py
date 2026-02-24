


class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

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