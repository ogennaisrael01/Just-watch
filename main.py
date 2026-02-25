from fastapi import FastAPI
from fastapi.responses import Response

from src.apps.users.api.router import user_router
from src.apps.users.exceptions.exception_handler import custom_exception_handler, CustomException

app = FastAPI(
    debug=True, 
    title="Just-Watch",
    description="A platform for your movies. Get AI recommendation")

@app.get('/health', status_code=200)
def health():
    return Response(content="OK", media_type="text/plain")



app.include_router(user_router)
app.add_exception_handler(CustomException, custom_exception_handler)

