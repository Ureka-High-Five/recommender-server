from fastapi import APIRouter
from pydantic import BaseModel
from app.services import user_service

router = APIRouter()

# ✅ 응답 DTO: userVector (string 형태로)
class FastApiOnboardingResponseDto(BaseModel):
    userVector: str

# ✅ 요청 처리
@router.post("/user/preferences", response_model=FastApiOnboardingResponseDto)
def onboarding(genre_map: dict[str, int]):
    user_vector_str = user_service.init_user_vector(genre_map)
    return FastApiOnboardingResponseDto(userVector=user_vector_str)
