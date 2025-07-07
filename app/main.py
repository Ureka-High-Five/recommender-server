from fastapi import FastAPI
from app.settings import settings

app = FastAPI(
    title="recommender server",
)

@app.get("/")
def read_root():
    return {
        "env": settings.DB_URL,
    }