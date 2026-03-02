# load apps and declearative base

from .apps.users.models.auth_models import User
from .apps.users.models.message_model import Message
from .config.database.base import Base
from .apps.movies.models.movie_model import MovieSearch, WatchList, Rate


from fastapi import FastAPI
from fastapi_cache import F
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi.middleware.cors import CORSMiddleware

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
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

app.add_middleware(
    SlowAPIMiddleware
)
