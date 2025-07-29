import asyncio
from contextlib import asynccontextmanager
from functools import partial
from logging import getLogger
from app.logger import setup_logging

import asyncpg
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.word2vec_model import Word2VecModel
from app.repositories.action_log_repository import ActionLogRepository
from app.repositories.postgresql_repository import get_genres_by_content_id
from app.repositories.user_weight_repository import UserWeightRepository
from app.router import recommend, content, scheduler_router, user, embedding
from app.services.consumer import start_consumer
from app.services.redis import init_redis, close_redis
from app.router import test_log
from app.services.scheduler_service import resize_weight
from app.settings import settings

scheduler = BackgroundScheduler(timezone='Asia/Seoul')
setup_logging()
logger = getLogger(__name__)
MONGO_URI = f"mongodb://{settings.MONGO_DB_HOST}:{settings.MONGO_DB_PORT}/{settings.MONGO_DB_NAME}"

async def start_rabbitmq_consumer():
    print("🚀 RabbitMQ Consumer 시작")
    return asyncio.create_task(start_consumer())


async def load_w2v(app: FastAPI):
    Word2VecModel.load_model(settings.W2V_MODEL_PATH)
    print("✅ Word2Vec 모델 로드 완료")

    # MongoDB 연결
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    app.state.mongo_client = mongo_client
    action_log_repo = ActionLogRepository(mongo_client)
    user_weight_repo = UserWeightRepository(mongo_client)

    # PostgreSQL 연결
    pg_pool = await asyncpg.create_pool(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        user=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
    )
    app.state.pg_pool = pg_pool
    print("✅ PostgreSQL 연결 완료")

    # resize_weight를 위한 스케줄링 함수 정의
    async def schedule_resize_weight():
        await resize_weight(
            action_log_repo,
            user_weight_repo,
            partial(get_genres_by_content_id, pg_pool),
        )

    loop = asyncio.get_running_loop()

    def schedule_resize_weight_wrapper():
        asyncio.run_coroutine_threadsafe(schedule_resize_weight(), loop)

    scheduler.add_job(schedule_resize_weight_wrapper, "cron", hour=3, minute=0)
    scheduler.start()
    print("✅ APScheduler 설정 완료")


@asynccontextmanager
async def lifespan(app: FastAPI):

    await load_w2v(app)

    await init_redis()

    rabbitmq_task = await start_rabbitmq_consumer()

    yield

    await app.state.pg_pool.close()
    print("🛑 앱 종료 중...")
    rabbitmq_task.cancel()
    await close_redis()
    print("🧹 자원 정리 완료")


app = FastAPI(
    title="recommender server",
    lifespan=lifespan,
    debug=True
)

app.include_router(recommend.router)
app.include_router(content.router)
app.include_router(user.router)
app.include_router(embedding.router)
app.include_router(scheduler_router.router)
app.include_router(test_log.router)


@app.get("/")
def read_root():
    return {"env": settings.DB_NAME}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
