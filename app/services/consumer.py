from app.settings.local import settings
import aio_pika

QUEUE_NAME = "recommendation.weight.update"


async def start_consumer():
    amqp_url = (
        f"amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}"
        f"@{settings.RABBITMQ_URL}:{settings.RABBITMQ_PORT}/"
    )
    connection = await aio_pika.connect_robust(amqp_url)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    print(f"📡 Waiting for messages on queue: {QUEUE_NAME}")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                body = message.body.decode()
                print(f"📥 Received: {body}")
                # try:
                #     data = json.loads(body)
                #     update_user_weight(
                #         data,
                #         repo=UserWeightRepository(mongo_client=settings.MONGO_CLIENT),
                #     )
                # except Exception as e:
                #     print(f"Rabbit MQ로부터의 메세지를 처리하는데 실패하였습니다.: {e}")
