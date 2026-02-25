from slowapi import _rate_limit_exceeded_handler
from slowapi.errors  import RateLimitExceeded

from fastapi import Request


async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    return _rate_limit_exceeded_handler(request, exc)