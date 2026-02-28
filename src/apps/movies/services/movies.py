import requests

from .utils import (
    get_secret_base_url, 
    check_movie_in_history, 
)
from src.config.settings import DEFAULT_PAGE
from src.config.database.setup import get_db
from src.apps.users.exceptions import UserNotFoundException
from ..exceptions.exceptions import FailedToSave
from .crud import save_history, delete_history, list_history
from .tmdb import get_movie_detail

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder


class MovieService:

    @staticmethod
    async def list_movies(page: int | None = None):
        """ 
        A view to list TMDB popular movies with pagination
        Implemented cache to ensure that i dont have to hit TMDB database on every request
        """
        if page is None:
            page = DEFAULT_PAGE
        
    
        api_key, base_url = await get_secret_base_url()
        request_path = f"{base_url}movie/popular"

        request_params = {
            "api_key": api_key,
            "page": page
        }
        response = requests.get(request_path, params=request_params)
        response.raise_for_status()

        result = response.json()
        return result 

    @staticmethod
    async def search_movies(query: str, page: int | None = None):
        """ 
            A view handling movie search 
        """
        if page is None:
            page = DEFAULT_PAGE

        api_key, base_url = await get_secret_base_url()
        request_params = {
            "api_key": api_key,
            "query": query,
            "page": page
        }
        request_path = base_url + "search/movie"
        response = requests.get(url=request_path, params=request_params)
        response.raise_for_status()

        result = response.json()
        return result
    
    @staticmethod
    async def movie_detail(current_user, movie_id: int, append_to_response: dict | None, 
                           db: AsyncSession = Depends(get_db)):
        

        user_id = getattr(current_user, "user_id")
        if user_id is None:
            raise UserNotFoundException(
                message="User not found",
                errors="Failed to get user pk",
                code=404
            )
        requests_params = {}
        if append_to_response is not None:
            requests_params.update({"append_to_response": append_to_response})
    
        result = await get_movie_detail(movie_id=movie_id, query_params=requests_params)
        return_movie_id = result['id'] 
        found, _ = await check_movie_in_history(user_id=user_id, movie_id=return_movie_id, db=db)
        if not found:
            # Save the movie in user search history
            new_history = await save_history(db=db, result=result, current_user=current_user)
            if new_history.movie_id:
                return result
            raise FailedToSave(message="failed to save", errors="Failed to save new search history", code=400)
        return result

    @staticmethod
    async def delete_search_history(current_user, movie_id: int, db: AsyncSession = Depends(get_db)):
    
        deleted_movie = await delete_history(
            db=db,
            user=current_user,
            movie_id=movie_id
        )

        if not deleted_movie:
            raise ValueError("Failed to deleted movie")
        
        if deleted_movie > 0:
            return deleted_movie

    @staticmethod
    async def list_search_histories(current_user, db: AsyncSession = Depends(get_db)):
        histories = await list_history(db, current_user)
        return [jsonable_encoder(history) for history in histories]
        