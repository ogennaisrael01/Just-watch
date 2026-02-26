
from src.apps.users.exceptions.exception_handler import CustomException


class APIKeyNotFOundError(CustomException):
    pass
    
    
class FailedToSave(CustomException):
    pass

class PemissionDenied(CustomException):
    message="Pemission not granted"
    errors="You are not pemitted to perform this action"
    code=403