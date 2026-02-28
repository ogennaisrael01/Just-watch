from pydantic import BaseModel, Field

from src.apps.users.models.auth_models import User

import uuid 

from typing import Optional, Any

class AppendToResponse(BaseModel):
    videos: bool | None = None
    credits: bool | None = None
    recommendations: bool | None = None 
    similar: bool | None = None 



class MovieSearchSchema(BaseModel):
    movie_id: int 
    movie_title: str
    owner_id: uuid.UUID = None

    release_date: str | None = None
    poster_path: str | None = None

    owner: Any

class WatchListSchema(BaseModel):
    movie_id: int
    owner_id: uuid.UUID


class RatingSchema(BaseModel):
    score: int = Field(ge=1, le=5)



    
