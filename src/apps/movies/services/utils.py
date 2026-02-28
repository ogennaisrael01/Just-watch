from src.config.settings import base_setting
from ..models.movie_model import MovieSearch, WatchList, Rate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.apps.movies.exceptions import APIKeyNotFOundError

async def get_secret_base_url() -> tuple[str]:
    api_key = getattr(base_setting, "TMDB_API_KEY")
    base_url = getattr(base_setting, "BASE_URL")

    if api_key is None or base_url is None:
        raise APIKeyNotFOundError(
            message="API Key or BASE URL Not Found",
            errors="This request requires a TMDB API Secret key",
            code=404
        )
    return api_key, base_url

async def check_movie_in_history(user_id, movie_id: int, db: AsyncSession) -> tuple[bool, MovieSearch | str]:
    if movie_id is None:
        raise ValueError("Movie id not provided")
    
    stmt = select(MovieSearch).where((MovieSearch.movie_id == movie_id), (MovieSearch.owner_id == user_id))

    query = await db.execute(stmt)
    result = query.scalar_one_or_none()
    if result is not None:
        return True, result
    return False, "Not Found"    

async def check_movie_in_watchlist(user, movie_id, db: AsyncSession) -> bool:
    stmt = select(WatchList).where(WatchList.movie_id == movie_id, WatchList.owner == user)

    query = await db.execute(stmt)

    result = query.scalar_one_or_none()
    if result is None:
        return False
    return True

async def check_rated_movie(current_user, movie_id: int, db: AsyncSession):
    stmt = select(Rate).where((Rate.movie_id == movie_id), (Rate.owner == current_user))
    query = await db.execute(stmt)

    result = query.scalar_one_or_none()
    if result is None:
        return False
    return True


