from .v1 import router as movie_router
from .watchlist_v1 import router as watchlist_router
from .rating_v1 import router as rating_router


__all__ = [
    "movie_router",
    "watchlist_router",
    "rating_router"
    
]