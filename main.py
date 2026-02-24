from fastapi import FastAPI
from fastapi.responses import Response


app = FastAPI(
    debug=True, 
    title="Just-Watch",
    description="A platform for your movies. Get AI recommendation")

@app.get('/health', status_code=200)
def health():
    return Response(content="OK", media_type="text/plain")



