from fastapi import APIRouter
from pydantic import BaseModel
from app.services import user_service

router = APIRouter()

class FastApiOnboardingResponseDto(BaseModel):
    userVector: str

@router.post("/user/preferences", response_model=FastApiOnboardingResponseDto)
def onboarding(genre_map: dict[str, int]):
    user_vector_str = user_service.init_user_vector(genre_map)
    return FastApiOnboardingResponseDto(userVector=user_vector_str)
