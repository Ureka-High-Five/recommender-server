from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.word2vec_model import Word2VecModel
from app.repositories.action_log_repository import ActionLogRepository
from app.repositories.user_weight_repository import UserWeightRepository
from app.services.redis import init_redis, close_redis
from app.services.scheduler_service import resize_weight
from app.settings import settings
from contextlib import asynccontextmanager
from app.router import recommend, content, user, embedding
from app.services.consumer import start_consumer
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

async def start_rabbitmq_consumer():
    print("🚀 RabbitMQ Consumer 시작")
    return asyncio.create_task(start_consumer())

@asynccontextmanager
def load_word2vec():
    mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
    action_log_repo = ActionLogRepository(mongo_client)
    user_weight_repo = UserWeightRepository(mongo_client)
    Word2VecModel.load_model(settings.W2V_MODEL_PATH)
    print("✅ Word2Vec 모델 로드 완료")

    def schedule_resize_weight():
        asyncio.create_task(resize_weight(action_log_repo, user_weight_repo))

    scheduler.add_job(schedule_resize_weight, "cron", hour=3, minute=0)
    scheduler.start()
    print("✅ APScheduler 설정 완료")

@asynccontextmanager
async def lifespan(app: FastAPI):

    load_word2vec()

    await init_redis()

    rabbitmq_task = await start_rabbitmq_consumer()

    yield

    print("🛑 앱 종료 중...")
    rabbitmq_task.cancel()
    await close_redis()
    print("🧹 자원 정리 완료")

app = FastAPI(
    title="recommender server",
    lifespan=lifespan,
)

app.include_router(recommend.router)
app.include_router(content.router)
app.include_router(user.router)
app.include_router(embedding.router)

@app.get("/")
def read_root():
    return {"env": settings.DB_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)