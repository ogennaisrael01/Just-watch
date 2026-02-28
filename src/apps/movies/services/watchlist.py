from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from src.config.database.setup import get_db
from src.apps.movies.services.utils import (
    check_movie_in_watchlist, 
    check_movie_in_history
)
from src.apps.movies.services.tmdb import get_movie_detail
from src.apps.movies.services.crud import (
    save_history, 
    save_watchlist,
    list_watchlist,
    delete_watchlists
)

class WatchListService:

    @staticmethod
    async def add_movie_to_watchlist(current_user, movie_id: int, db: AsyncSession):
        movie_detail = await get_movie_detail(movie_id=movie_id, query_params={})

        watchlist  = await check_movie_in_watchlist(current_user, movie_id, db)

        if not watchlist:
            await save_watchlist(current_user=current_user, movie_id=movie_id, db=db)
            movie_history, _ = await check_movie_in_history(current_user.user_id, movie_id, db)

            if not movie_history:
                await save_history(db=db, result=movie_detail, current_user=current_user)

        return movie_detail
    
    @staticmethod
    async def list_user_watchlist(current_user, db: AsyncSession):
        watchlist = await list_watchlist(current_user=current_user, db=db)
        return [jsonable_encoder(watch) for watch in watchlist]
    
    @staticmethod
    async def fetch_one_watchlist(current_user, db: AsyncSession, movie_id):
        
        watchlist = await list_watchlist(
            current_user=current_user, db=db, movie_id=movie_id
        )
        if watchlist is None:
            raise ValueError("Faild to fetch result. No movie found")
        
        return watchlist

    @staticmethod
    async def destroy_watchlists(current_user, db: AsyncSession, movie_id: int | None, email: str | None):
        """ delete a single watchlist or clear or watchlist for the authenticated user """
        if movie_id is None and email is None:
            raise ValueError("email must be provided for bulk delete")
        
        if email is not None and email != current_user.email:
            raise ValueError("Unauthorized to delete watchlist for this user")
        
        deleted_rows = await delete_watchlists(current_user, db, movie_id)
        if not deleted_rows:
            raise ValueError("No movie found in watchlist")
        return deleted_rows