from fastapi import FastAPI
from app.settings import settings
from contextlib import asynccontextmanager
from app.models.word2vec_model import Word2VecModel
from app.router import recommend, content, user, embedding

@asynccontextmanager
async def load_w2v(app: FastAPI):
    # 앱 시작 시
    Word2VecModel.load_model(settings.W2V_MODEL_PATH)
    print("✅ Word2Vec 모델 로드 완료")
    yield
    # 앱 종료 시
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
