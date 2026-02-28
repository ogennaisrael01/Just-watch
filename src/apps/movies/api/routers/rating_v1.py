from fastapi import (
    APIRouter, Depends, 
    Path, Body, HTTPException, 
    status, Request
)

from sqlalchemy.ext.asyncio import AsyncSession

from .v1 import User, UserService, get_db, limiter,cache
from ...schemas.movie_schema import RatingSchema
from ...services.ratings import RatingService

router = APIRouter(
    prefix='/v1/p3', tags=["Rating"]
)


@router.get("/movie-ratings/")
@limiter.limit('10/minute')
@cache(expire=60 * 60)
async def fetch_ratings(
        request: Request,
        current_user: User = Depends(UserService.get_current_user),
        db: AsyncSession = Depends(get_db)
):
    
    try:
        result = await RatingService.retrieve_rating(
            current_user=current_user,
            db=db
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return {
        "status": "success",
        "result": result
    }
    


@router.post("/movie/{movie_id}/rate", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def rate_movie(
    request: Request,
    movie_id: int = Path(...),
    data: RatingSchema = Body(...),
    current_user: User = Depends(UserService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rating_data = data.model_dump()
    score = rating_data.get("score")


    if score is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="score is required to rate this movie"
        )
    
    try:
        result = await RatingService.rate_movie(
            current_user=current_user, db=db, movie_id=movie_id, score=score
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return result

@router.patch("/movie/{movie_id}/rate")
@limiter.limit('10/minute')
async def update_rated_movie(
    request: Request,
    movie_id: int = Path(...),
    data: RatingSchema = Body(...),
    current_user: User = Depends(UserService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    data_dump = data.model_dump()
    score = data_dump.get("score")

    if 1 <= score <=10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="rating can only be between 1 and 10"
        )
    
    try:
        result = await  RatingService.update_rating_score(
            current_user=current_user,
            db=db,
            movie_id=movie_id,
            updated_score=score
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return {
        "status": "success",
        "updated_row(s)": result
    }



@router.delete('/movie-ratings/')
@router.delete('/movie/{movie_id}/rate')
async def deleted_rated_movie(
        current_user: User = Depends(UserService.get_current_user),
        db: AsyncSession = Depends(get_db),
        movie_id: int | None = None

):
    try:
        result = await RatingService.delete_score(
            current_user=current_user,
            db=db,
            movie_id=movie_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return {
        "status": "success,",
        "deleted_row(s)": result
    }



