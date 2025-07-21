from fastapi import FastAPI

from app.models.word2vec_model import Word2VecModel
from app.repositories.action_log_repository import ActionLogRepository
from app.repositories.user_weight_repository import UserWeightRepository
from app.settings import settings
from contextlib import asynccontextmanager
from app.router import recommend, content, user, embedding
from app.services.consumer import start_consumer
import asyncio
from app.services.scheduler_service import resize_weight
from apscheduler.schedulers.background import BackgroundScheduler
from motor.motor_asyncio import AsyncIOMotorClient

scheduler = BackgroundScheduler()

@asynccontextmanager
async def load_w2v(app: FastAPI):
    mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
    action_log_repo = ActionLogRepository(mongo_client)
    user_weight_repo = UserWeightRepository(mongo_client)

    Word2VecModel.load_model(settings.W2V_MODEL_PATH)
    print("✅ Word2Vec 모델 로드 완료")

    def schedule_resize_weight():
        asyncio.create_task(resize_weight(action_log_repo, user_weight_repo))

    consumer_task = asyncio.create_task(start_consumer())
    scheduler.add_job(schedule_resize_weight, "cron", hour=3, minute=0)
    scheduler.start()
    print("✅ APScheduler 설정 완료")

    yield

    consumer_task.cancel()
    print("🛑 앱 종료됨")

app = FastAPI(
    title="recommender server",
    lifespan=load_w2v,
)

app.include_router(recommend.router)
app.include_router(content.router)
app.include_router(user.router)
app.include_router(embedding.router)

@app.get("/")
def read_root():
    return {
        "env": settings.DB_NAME,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)