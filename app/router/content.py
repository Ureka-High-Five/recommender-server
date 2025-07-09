from fastapi import APIRouter
from app.repositories import content_repository

router = APIRouter()

@router.get("/init-embedding")
def recommend_shorts():
  return content_repository.init_vector()