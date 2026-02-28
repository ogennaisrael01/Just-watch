from fastapi import (APIRouter, status, 
                     HTTPException, Depends, Request,
                     Query, Path
)
from fastapi.encoders import jsonable_encoder

from .v1 import limiter, cache, User, UserService, get_db
from src.apps.movies.services.recommedation_service import RecommendationService

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix='/v1/p3', tags=["Recommendation"]
)


@router.get('/recommendations-for_you/', status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
@cache(expire=60 * 60)
async def personalized_resommendation_for_user(
    request: Request,
    current_user: User = Depends(UserService.get_current_user),
    db: AsyncSession = Depends(get_db),
    page: int = Query(description="pagination")
):
    
    try:
        recommendation_service = RecommendationService(
            current_user=current_user,
            db=db
        )

        result = await recommendation_service.get_recommendations_for_user(page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return {
        "status": "success",
        "result": result
    }


@router.get("/movie/{movie_id}/recommendations")
@limiter.limit("10/minute")
@cache(expire=60 * 60)
async def recommend_similar_movies(
    request: Request,
    movie_id: int = Path(...),
    page: int | None = None
):
    try:
        recommendation_service = RecommendationService()

        result = await recommendation_service.recommend_similar_movies(page=page, movie_id=movie_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return {
        "status": "success",
        "result": result
    }