# load apps and declearative base

from .apps.users.models.auth_models import User
from .config.database.base import Base


from fastapi import FastAPI
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

app = FastAPI(
    debug=True, 
    title="Just-Watch",
    description="A platform for your movies. Get AI recommendation")

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

app.state.limiter = limiter

app.add_middleware(
    SlowAPIMiddleware
)

