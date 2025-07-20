from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pymongo import MongoClient
from app.dto.user_dto import UserActionRequestDto
from app.repositories.user_weight_repository import UserWeightRepository
from app.services import user_service
from app.settings import settings

router = APIRouter()

class FastApiOnboardingResponseDto(BaseModel):
    userVector: str

mongo_client = MongoClient(settings.MONGO_URL)

# Dependency
def get_prefer_info_repository():
    return UserWeightRepository(mongo_client)

@router.post("/user/preferences", response_model=FastApiOnboardingResponseDto)
def onboarding(genre_map: dict[str, int]):
    user_vector_str = user_service.init_user_vector(genre_map)
    return FastApiOnboardingResponseDto(userVector=user_vector_str)

@router.patch("/user/action")
def user_action(req : UserActionRequestDto,
                repo: UserWeightRepository = Depends(get_prefer_info_repository)):
    user_service.process_user_action(req, repo)

