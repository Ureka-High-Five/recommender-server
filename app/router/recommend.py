from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.services import recommend_service

router = APIRouter()

# Request Body 정의
class RecommendRequest(BaseModel):
    vector: str

@router.post("/contents")
def recommend_contents(
  request: RecommendRequest,     # ✅ body
  count: int = Query(...)      # ✅ query parameter
):
  vector = request.vector
  return recommend_service.contents(vector, count)

@router.get("/shorts")
def recommend_shorts(user_id : int):
  return recommend_service.shorts(user_id)