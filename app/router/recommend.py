# app/router/recommend.py

from fastapi import APIRouter
from app.services import recommend_service

router = APIRouter(
    prefix="/recommend",
)

@router.get("/contents")
def recommend_contents(user_id : int):
  return recommend_service.contents(user_id)

@router.get("/shorts")
def recommend_shorts(user_id : int):
  return recommend_service.shorts(user_id)