from typing import Optional
from fastapi.encoders import jsonable_encoder

from .crud import list_history
from .tmdb import discover_movies, similar_movies
from sqlalchemy.ext.asyncio import AsyncSession

from asyncio.log import logger

class RecommendationService:
    def __init__(self, current_user: Optional[str] = None, db: Optional[AsyncSession] = None):
        self.current_user = current_user
        self.db = db
        
    async def recomendation_repository(self) -> dict:
        user_activity_history = await list_history(current_user=self.current_user, db=self.db)

        user_activity = [jsonable_encoder(activity) for activity in user_activity_history[:20]]
        # group genres
        genre = {}
        strength = 5
        for data in user_activity:
            history = data["MovieSearch"]
            genre_ids = history["genre_ids"]
            for id in genre_ids:
                if id in genre:
                    genre[id] += strength
                else:
                    genre[id] = strength
        return genre

    async def get_recommendations_for_user(self, page: int):
        recommendation_engine = await self.recomendation_repository()
        recommendation_genres = []
        for key, value in recommendation_engine.items():
            # We filter genre which strength is greater than 5
            if value >= 10:
                recommendation_genres.append(str(key))
            else:
                logger.info(f"Genre {key} has strength {value}, which is not greater than 10, so it will be filtered out.")
        params = {
            "with_genres": ",".join(recommendation_genres),
            "sort_by": "popularity.desc",
            "page": page
        }
        result = await discover_movies(query_params=params)

        return result
    
    async def recommend_similar_movies(self, page: int, movie_id:int):
        params = {
            "page": page
        }
        result = await similar_movies(movie_id=movie_id, query_params=params)
        
        return result

