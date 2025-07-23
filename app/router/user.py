from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pymongo import MongoClient
from app.dto.user_dto import UserActionRequestDto
from app.repositories.user_weight_repository import UserWeightRepository
from app.services import user_service
from app.services.redis import save_user_vector
from app.settings import settings

router = APIRouter()

class OnboardingRequestDto(BaseModel):
    user_id: int
    genre_map: dict[str, int]

class FastApiOnboardingResponseDto(BaseModel):
    userVector: str

mongo_client = MongoClient(settings.MONGO_URL)

# Dependency
def get_prefer_info_repository():
    return UserWeightRepository(mongo_client)

@router.post("/user/preferences", response_model=FastApiOnboardingResponseDto)
def onboarding(req: OnboardingRequestDto):
    user_vector_str = user_service.init_user_vector(req.genre_map)
    save_user_vector(req.user_id, user_vector_str)
    return FastApiOnboardingResponseDto(userVector=user_vector_str)

@router.patch("/user/action")
async def user_action(req : UserActionRequestDto,
                repo: UserWeightRepository = Depends(get_prefer_info_repository)):
    user_service.process_user_action(req, repo)

