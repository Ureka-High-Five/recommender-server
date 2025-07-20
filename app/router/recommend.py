from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.services import recommend_service

router = APIRouter()

# Request Body 정의
class RecommendRequest(BaseModel):
    vector: str

@router.post("/contents")
def recommend_contents(
  request: RecommendRequest,
  count: int = Query(...)
):
  user_vector = request.vector
  return recommend_service.recommend_contents_by_user(user_vector, count)
