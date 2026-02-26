from ..models.movie_model import MovieSearch, WatchList
from ..schemas.movie_schema import MovieSearchSchema, User, WatchListSchema
from src.apps.users.exceptions import UserNotFoundException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select


async def save_history(db: AsyncSession,  result: dict, current_user):
    movie = MovieSearchSchema(
                movie_id=result["id"],
                movie_title=result["original_title"],
                owner_id=current_user.user_id,
                release_date=result["release_date"],
                poster_path=result['poster_path'],
                owner=current_user
            )

    movie_search = movie.model_dump()

    new_history = MovieSearch(**movie_search)
    db.add(new_history)
    await db.commit()
    await db.refresh(new_history)
    return new_history


async def delete_history(db: AsyncSession, user: User, movie_id: int):

    if user is None:
        raise UserNotFoundException(
            message="user not found",
            errors="Errors getting user detail",
            code=404
        )

    stmt = delete(MovieSearch).where(
        (MovieSearch.owner_id == user.user_id) | (MovieSearch.owner == user), 
        (MovieSearch.movie_id == movie_id)
    )
    query = await db.execute(stmt)
    await db.commit()
    if query.rowcount == 0:
        return False
    
    return query.row_count

async def list_history(db: AsyncSession, current_user):
    stmt = select(MovieSearch).where((MovieSearch.owner_id == current_user.user_id)|
                                     (MovieSearch.owner == current_user ))

    query = await db.execute(stmt)
    results = query.fetchall()

    yield results 


async def save_watchlist(current_user: User, movie_id: int, db: AsyncSession):
    watchlist = WatchListSchema(
        movie_id=movie_id,
        owner_id=current_user.user_id
    )
    watchlist.model_dump()

    new_watchlist = WatchList(owner=current_user, **watchlist)
    db.add(new_watchlist)
    await db.commit()
    await db.refresh(new_watchlist)
    return new_watchlist
    
