from fastapi import FastAPI

from app.models.word2vec_model import Word2VecModel
from app.settings import settings
from contextlib import asynccontextmanager
from app.router import recommend, content, user, embedding
from app.services.consumer import start_consumer
import asyncio
from app.services import scheduler_service
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def resize_user_weight():
    scheduler_service.resize_weight()

@asynccontextmanager
async def load_w2v(app: FastAPI):
    Word2VecModel.load_model(settings.W2V_MODEL_PATH)
    print("✅ Word2Vec 모델 로드 완료")

    # RabbitMQ consumer 백그라운드 실행
    consumer_task = asyncio.create_task(start_consumer())
    scheduler.add_job(resize_user_weight, "cron", hour=3, minute=0)  # 매일 새벽 3시
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