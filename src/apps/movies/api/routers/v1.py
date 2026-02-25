from fastapi import APIRouter


router = APIRouter(prefix="/v1/movies", tags=["Movies"])

@router.get("/")
def tmdb_movies(query: int | None = None):
    pass