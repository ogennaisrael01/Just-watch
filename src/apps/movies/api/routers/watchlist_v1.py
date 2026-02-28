from .v1 import User, UserService, get_db

from fastapi_cache.decorator import cache
from fastapi import (
    Request,  Depends, 
    Path, HTTPException, 
    status, APIRouter, Query
)

from sqlalchemy.ext.asyncio import AsyncSession

from src.manage import limiter
from src.apps.movies.services.watchlist import WatchListService

from typing import Optional

router = APIRouter(
    prefix='/v1/p3', tags=["Watch-List"]
)

@router.post("/watch-list/")
@limiter.limit("10/minute")
async def add_watchlist(
    request: Request, current_user: User =  Depends(UserService.get_current_user),
    db: AsyncSession = Depends(get_db), movie_id: int = Path(...)):

    try:
        result =  await WatchListService.add_movie_to_watchlist(
            current_user=current_user, movie_id=movie_id, db=db
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return result


@router.get("/watch-list/", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
@cache(expire=60 * 20)
async def list_watchlist(
    request: Request, current_user: User =  Depends(UserService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await WatchListService.list_user_watchlist(current_user=current_user, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return {
        "status": "success",
        "results": result
    }

@router.get("/watch-list/{movie_id}", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
@cache(expire=60 * 180)
async def retreive_watchlist(
    request: Request, current_user: User =  Depends(UserService.get_current_user),
    db: AsyncSession = Depends(get_db), movie_id: int = Path(...)
):
    
    try:
        result = await WatchListService.fetch_one_watchlist(
            current_user=current_user, db=db, movie_id=movie_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return result


@router.delete('/watch-list')
@router.delete('/watch-list/{movie_id}')
async def delete_watchlist(
        current_user: User = Depends(UserService.get_current_user), 
        db: AsyncSession = Depends(get_db), movie_id: int | None = None,
        email: Optional[str | None] = Query(description="email must be provided for bulk delete")
    ):

    try:
        result = await WatchListService.destroy_watchlists(
            current_user=current_user, db=db, movie_id=movie_id, email=email
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return {
        "status": "success",
        "deleted_row(s)": result
    }