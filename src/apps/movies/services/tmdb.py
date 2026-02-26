import functools
import requests

from .utils import get_secret_base_url

@functools.lru_cache(maxsize=200)
async def get_movie_detail(movie_id: int, query_params: dict | None = None) -> dict:
    api_key, base_url  = await get_secret_base_url()

    if query_params is None or not query_params.get("api_key"):
        query_params.update({"api_key": api_key})
    response = requests.get(url=base_url + f"movie/{movie_id}", params=query_params)

    response.raise_for_status()
    result = response.json()

    return result