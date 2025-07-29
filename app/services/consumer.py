import json
import logging

from app.repositories.user_weight_repository import UserWeightRepository
from app.repositories.action_log_repository import ActionLogRepository
from app.services.user_service import process_user_action, update_user_weight
from app.settings.local import settings
import aio_pika
from motor.motor_asyncio import AsyncIOMotorClient


QUEUE_NAME = "recommendation.weight.update"
MONGO_URI = f"mongodb://{settings.MONGO_DB_HOST}:{settings.MONGO_DB_PORT}/{settings.MONGO_DB_NAME}"

async def start_consumer():
    amqp_url = (
        f"amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}"
        f"@{settings.RABBITMQ_URL}:{settings.RABBITMQ_PORT}/"
    )
    connection = await aio_pika.connect_robust(amqp_url)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    mongo_client = AsyncIOMotorClient(MONGO_URI)
    user_repo = UserWeightRepository(mongo_client)
    action_log_repo = ActionLogRepository(mongo_client)
    print(f"📡 Waiting for messages on queue: {QUEUE_NAME}")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                body = message.body.decode()
                print(f"📥 Received: {body}")

                data = json.loads(body)

                try:
                    await update_user_weight(
                        data,
                        user_repo,
                    )
                except Exception as e:
                    logging.error(f"가중치 업데이트 실패 : {e}")
                    await action_log_repo.mark_status(
                        collection_names = ["action_log", "managed_action_log"],
                        doc_id = data["id"],
                        status = "FAIL"
                    )
                    await message.nack(requeue=False)
                    continue

                try:
                    await process_user_action(
                        data,
                        user_repo,
                        action_log_repo
                    )
                except Exception as e:
                    logging.error(f"사용자 벡터 갱신 실패 : {e}")
                    await action_log_repo.mark_status(
                        collection_names = ["action_log", "managed_action_log"],
                        doc_id = data["id"],
                        status = "FAIL"
                    )
                    await message.nack(requeue=False)