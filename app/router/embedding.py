from typing import List
from fastapi import APIRouter, Body
from app.services import embedding_service

router = APIRouter()

@router.post("/embedding-by-genre")
def embedding_by_genre(genres: List[str] = Body(..., embed=True)):
    return embedding_service.calc_by_genre(genres)