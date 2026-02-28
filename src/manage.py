# load apps and declearative base

from .apps.users.models.auth_models import User
from .config.database.base import Base
from .apps.movies.models.movie_model import MovieSearch, WatchList, Rate


from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend())
    yield

app = FastAPI(
    lifespan=lifespan,
    debug=True, 
    title="Just-Watch",
    description="A platform for your movies. Get AI recommendation")

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

app.state.limiter = limiter

app.add_middleware(
    SlowAPIMiddleware
)

