from ..models.movie_model import MovieSearch, WatchList, Rate
from ..schemas.movie_schema import MovieSearchSchema, User, WatchListSchema
from src.apps.users.exceptions import UserNotFoundException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update


async def save_history(db: AsyncSession,  result: dict, current_user):
    movie = MovieSearchSchema(
                movie_id=result["id"],
                movie_title=result["original_title"],
                owner_id=current_user.user_id,
                release_date=result["release_date"],
                poster_path=result['poster_path'],
                genre_ids=[genre["id"] for genre in result["genres"]],
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
    
    return query.rowcount


async def list_history(db: AsyncSession, current_user):
    stmt = select(MovieSearch).where((MovieSearch.owner_id == current_user.user_id)|
                                     (MovieSearch.owner == current_user ))

    query = await db.execute(stmt)
    results = query.mappings().all()
    return results 


async def save_watchlist(current_user: User, movie_id: int, db: AsyncSession):
    watchlist = WatchListSchema(
        movie_id=movie_id,
        owner_id=current_user.user_id
    )
    watch = watchlist.model_dump()

    new_watchlist = WatchList(owner=current_user, **watch)
    db.add(new_watchlist)
    await db.commit()
    await db.refresh(new_watchlist)
    return new_watchlist
    
async def list_watchlist(current_user, db: AsyncSession, movie_id: int | None = None):
    if movie_id is not None:
        stmt = select(WatchList).where((WatchList.owner == current_user), (WatchList.movie_id == movie_id))
    else:
        stmt = select(WatchList).where((WatchList.owner == current_user))

    query = await db.execute(stmt)
    if movie_id is not None:
        result = query.scalar_one_or_none()
    else:
        result = query.mappings().all()

    return result

async def delete_watchlists(current_user, db: AsyncSession, movie_id: int | None = None):
    if movie_id is not None:
        stmt = delete(WatchList).where((WatchList.owner == current_user), (WatchList.movie_id == movie_id))
    else:
        stmt = delete(WatchList).where((WatchList.owner == current_user))

    query = await db.execute(stmt)
    await db.commit()
    if query.rowcount == 0:
        return False
    return query.rowcount

async def save_rating(current_user: User, movie_id: int, db: AsyncSession, score:int):
    rating = Rate(owner_id=current_user.user_id, movie_id=movie_id, 
        score=score
        )
    db.add(rating)
    await db.commit()
    await db.refresh(rating)
    return rating

async def update_rated_movie(current_user: User, movie_id: int, db: AsyncSession, updated_score: int):
    stmt = update(Rate).where(
        (Rate.movie_id == movie_id), 
        (Rate.owner == current_user)
        ).values(Rate.score == updated_score
    )

    query = await db.execute(stmt)
    await db.commit()

    if query.rowcount == 0:
        return False
    return query.rowcount

async def delete_rated_movie(current_user: User, movie_id: int | None, db: AsyncSession):
    if movie_id is None:
        stmt = delete(Rate).where(Rate.owner == current_user)
    else:
        stmt = delete(Rate).where((Rate.owner == current_user), (Rate.movie_id == movie_id))

    query = await db.execute(stmt)
    await db.commit()
    if query.rowcount == 0:
        return False
    return query.rowcount

async def fetch_rating(current_user: User, db: AsyncSession):
    stmt = select(Rate).where((Rate.owner == current_user ))

    query = await db.execute(stmt)
    ratings = query.mappings().all()

    if not ratings:
        return 0
    return ratings