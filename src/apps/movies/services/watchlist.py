from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from src.config.database.setup import get_db
from src.apps.movies.services.utils import (
    check_movie_in_watchlist, 
    check_movie_in_history
)
from src.apps.movies.services.tmdb import get_movie_detail
from src.apps.movies.services.crud import save_history, save_watchlist

class WatchListService:

    @staticmethod
    async def add_movie_to_watchlist(current_user, movie_id: int, db: AsyncSession = Depends(get_db)):
        movie_detail = await get_movie_detail(movie_id=movie_id, query_params=None)

        watchlist  = await check_movie_in_watchlist(current_user, movie_id, db)

        if not watchlist:
            await save_watchlist(current_user=current_user, movie_id=movie_id, db=db)
            movie_history, _ = await check_movie_in_history(current_user.user_id, movie_id, db)

            if not movie_history:
                await save_history(db=db, result=movie_detail, current_user=current_user)

        return movie_detail
        
    


