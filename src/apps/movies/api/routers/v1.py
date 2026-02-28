
from fastapi import APIRouter, HTTPException, status, Request, Depends, Query, Path
from fastapi_cache.decorator import cache
from fastapi.encoders import jsonable_encoder

from src.apps.movies.services.movies import MovieService
from src.apps.movies.schemas.movie_schema import MovieSearchSchema
from src.config.database.setup import get_db
from src.manage import limiter
from src.apps.users.models.auth_models import User
from src.apps.users.services.user_services import UserService

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional, List

router = APIRouter(prefix="/v1/p3", tags=["Movies"])

@router.get("/movie")
@limiter.limit("10/minute")
@cache(expire=60 * 180)
async def tmdb_popular_movies(request: Request, page: int = None):
    """ 
    A view to list TMDB popular movies with pagination
    Implemented cache to ensure that i dont have to hit TMDB database on every request
    """
    try:
        result = await MovieService.list_movies(page)   
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    return jsonable_encoder(result)

@router.get("/search/movie", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
@cache(expire=60 * 360)
async def tmdb_search_movies(request: Request, query: str, page: int | None = None):
    try:
        result = await MovieService.search_movies(query=query, page=page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return jsonable_encoder(result)

@router.get("/movie/{movie_id}")
@limiter.limit("10/minute")
@cache(expire=60 * 360)
async def tmdb_movie_details( request: Request, movie_id: int, 
    append: Optional[List[str]] = Query(default=None, description="comma(,) seperated list of argument to add to the request"),
    db: AsyncSession = Depends(get_db), current_user: User = Depends(UserService.get_current_user)
):


    if append is not None:
        append_to_response = ','.join(append)
    else:
        append_to_response = None

    try:
        result = await MovieService.movie_detail(
            movie_id=movie_id, append_to_response=append_to_response,
            db=db, current_user=current_user
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    return jsonable_encoder(result)


@router.delete("/movie/{movie_id}", status_code=status.HTTP_200_OK)
async def delete_saved_history(current_user: User = Depends(UserService.get_current_user), 
                               db: AsyncSession = Depends(get_db), movie_id: int = Path(...)):
    
    try:
        result = await MovieService.delete_search_history(
            current_user=current_user,
            movie_id=movie_id,
            db=db
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return result

@router.get("/history/")
@limiter.limit('10/munite')
@cache(expire=60 * 5)
async def list_search_history(
    request: Request,
    current_user: User= Depends(UserService.get_current_user), 
    db: AsyncSession = Depends(get_db)):

    try:
        result = await MovieService.list_search_histories(
            current_user, db
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return {"status": "success", "result": result}
