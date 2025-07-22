from fastapi import APIRouter, Request
from functools import partial
from app.repositories.action_log_repository import ActionLogRepository
from app.repositories.user_weight_repository import UserWeightRepository
from app.repositories.postgresql_repository import get_genres_by_content_id
from app.services.scheduler_service import resize_weight

router = APIRouter()

@router.post("/contents/resize-weight")
async def trigger_resize_weight(request: Request):
    # FastAPI app에서 공유 객체 가져오기
    pg_pool = request.app.state.pg_pool
    mongo_client = request.app.state.mongo_client

    action_log_repo = ActionLogRepository(mongo_client)
    user_weight_repo = UserWeightRepository(mongo_client)
    get_genres_func = partial(get_genres_by_content_id, pg_pool)

    # 실제 비동기 가중치 재계산 실행
    await resize_weight(action_log_repo, user_weight_repo, get_genres_func)

    return {"message": "ok"}
