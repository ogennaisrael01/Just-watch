from .v1 import router, User, UserService, get_db

from fastapi_cache.decorator import cache
from fastapi import Request,  Depends, Path, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.manage import limiter
from src.apps.movies.services.watchlist import WatchListService


@router.post("/watch-list/{movie_id}/")
@limiter.limit("10/minute")
async def add_watchlist(
    request: Request, current_user: User =  Depends(UserService.get_current_user),
    db: AsyncSession = Depends(get_db), movie_id: int = Path(...)):

    try:
        result = WatchListService.add_movie_to_watchlist(
            current_user=current_user, movie_id=movie_id, db=db
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return result
