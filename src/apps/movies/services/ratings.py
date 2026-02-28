from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from .tmdb import get_movie_detail
from .utils import check_rated_movie,  check_movie_in_history
from .crud import (
    save_rating, save_history, 
    update_rated_movie,
    delete_rated_movie,
    fetch_rating
)


class RatingService:
    @staticmethod
    async def rate_movie(current_user, db: AsyncSession, movie_id: int, score: int):
        movie = await get_movie_detail(movie_id=movie_id)
        rated_movie = await check_rated_movie(current_user, movie_id, db)
        if rated_movie:
            raise ValueError("You have rated this movie in the past, consider using the update method")

        in_history, _ = await check_movie_in_history(user_id=current_user.user_id, movie_id=movie_id, db=db)
        
        if not in_history:
            history = await save_history(db=db, result=movie)

        await save_rating(current_user=current_user, movie_id=movie_id, db=db, score=score)

        return movie

    @staticmethod
    async def update_rating_score(current_user, db: AsyncSession, movie_id: int, updated_score: int):

        try:
            updated_row = await update_rated_movie(
                current_user=current_user,
                db=db,
                movie_id=movie_id,
                updated_score=updated_score
            )
        except  Exception as e:
            raise ValueError("Error updating movie")
        return updated_row

    @staticmethod
    async def delete_score(current_user, db: AsyncSession, movie_id: int | None):
        deleted_rows = await delete_rated_movie(
            current_user=current_user,
            movie_id=movie_id,
            db=db
        )
        if not deleted_rows:
            return 0
        return deleted_rows
    

    @staticmethod
    async def retrieve_rating(current_user, db: AsyncSession):
        result  = await fetch_rating(
            current_user=current_user,
            db=db
        )
        if result == 0:
            return 0
        return [jsonable_encoder(rating) for rating in result]
    
    