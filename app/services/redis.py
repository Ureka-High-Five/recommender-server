import aioredis
from app.settings import settings

redis = None  # 전역 Redis 클라이언트

async def init_redis():
    global redis
    redis_url = f"redis://{settings.DEV_REDIS_HOST}:{settings.DEV_REDIS_PORT}"
    redis = await aioredis.from_url(redis_url, decode_responses=True)
    print(f"✅ Redis 연결 성공: {redis_url}")

async def close_redis():
    global redis
    if redis:
        await redis.close()
        redis = None
        print("🧹 Redis 연결 종료")

async def save_user_vector(user_id: int, value: str):
    await redis.set(str(user_id), value)
    print(f"✅ 🔐 Redis 저장 완료: {user_id} → {value}")
