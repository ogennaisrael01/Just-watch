from fastapi import Request
from fastapi.responses import Response
from fastapi_cache.decorator import cache


from src.apps.users.api.router import user_router, chat_box_router
from src.apps.movies.api.routers import (
    movie_router, watchlist_router, 
    rating_router, recommendation_router
)
from src.apps.users.exceptions.exception_handler import (
    custom_exception_handler, CustomException
)
from src.exception_handler import rate_limit_exception_handler

from slowapi.errors import RateLimitExceeded

import time
from . import manage

app = manage.app
limiter = manage.limiter


@app.get('/slow')
@cache(expire=60)
def slow():
    time.sleep(10)
    return {"status": "success"}


@app.get('/health', status_code=200)
@limiter.limit("2/minute")
def health(request: Request):
    return Response(content="OK", media_type="text/plain")


app.include_router(user_router)
app.include_router(movie_router)
app.include_router(watchlist_router)
app.include_router(rating_router)
app.include_router(recommendation_router)
app.include_router(chat_box_router)
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
