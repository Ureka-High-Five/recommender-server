from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from pymongo import MongoClient
from app.dto.user_dto import UserActionRequestDto
from app.repositories.user_weight_repository import UserWeightRepository
from app.services import user_service
from app.services.redis import save_user_vector
from app.settings import settings

router = APIRouter()

class OnboardingRequestDto(BaseModel):
    user_id: int = Field(..., alias="userId")
    genre_count: dict[str, int] = Field(..., alias="genreCount")

    class Config:
        allow_population_by_field_name = True

class FastApiOnboardingResponseDto(BaseModel):
    userVector: str

mongo_client = MongoClient(settings.MONGO_URL)

# Dependency
def get_prefer_info_repository():
    return UserWeightRepository(mongo_client)

@router.post("/user/preferences", response_model=FastApiOnboardingResponseDto)
async def onboarding(req: OnboardingRequestDto):
    user_vector_str = user_service.init_user_vector(req.genre_count)
    await save_user_vector(req.user_id, user_vector_str)
    return FastApiOnboardingResponseDto(userVector=user_vector_str)

@router.patch("/user/action")
async def user_action(req : UserActionRequestDto,
                repo: UserWeightRepository = Depends(get_prefer_info_repository)):
    user_service.process_user_action(req, repo)

