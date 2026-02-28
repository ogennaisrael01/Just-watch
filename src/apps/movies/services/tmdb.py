from fastapi_cache.decorator import cache
import requests

from .utils import get_secret_base_url

from typing import Optional


@cache(expire=60 * 180)
async def get_movie_detail(movie_id: int, query_params: dict | None = None) -> dict:
    api_key, base_url  = await get_secret_base_url()
    
    if query_params is None:
        query_params = {"api_key": api_key}
    else:
        query_params.update({"api_key": api_key})
    
    response = requests.get(url=base_url + f"movie/{movie_id}", params=query_params)

    response.raise_for_status()
    result = response.json()

    if result is None:
        raise ValueError("Movie not found")

    return result

@cache(expire=60 * 180)
async def discover_movies(query_params: dict | None = None):
    api_key, base_url  = await get_secret_base_url()
    
    if query_params is None:
        query_params = {"api_key": api_key}
    else:
        query_params.update({"api_key": api_key})
    
    response = requests.get(url=base_url + f"discover/movie", params=query_params)

    response.raise_for_status()
    result = response.json()
    if result["results"] is None:
        raise ValueError("Movie not found")

    return result

async def similar_movies(movie_id: int, query_params: dict | None = None):
    api_key, base_url  = await get_secret_base_url()
    
    if query_params is None:
        query_params = {"api_key": api_key}
    else:
        query_params.update({"api_key": api_key})
    
    response = requests.get(url=base_url + f"movie/{movie_id}/recommendations", params=query_params)

    response.raise_for_status()
    result = response.json()
    if result["results"] is None:
        raise ValueError("Movie not found")

    return result
