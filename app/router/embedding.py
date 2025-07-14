import json
from typing import List
from fastapi import APIRouter, Body
from app.services import embedding_service

router = APIRouter()

@router.post("/embedding-by-genre")
def embedding_by_genre(genres: List[str] = Body(..., embed=True)):
    json_string = json.dumps(embedding_service.calc_by_genre(genres).tolist())     # "[1.0, 2.0]"
    return {"vector": json_string}