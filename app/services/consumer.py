from app.settings.local import settings
import aio_pika

QUEUE_NAME = "recommendation.weight.update"

async def start_consumer():
    amqp_url = (
        f"amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}"
        f"@{settings.RABBITMQ_URL}:{settings.RABBITMQ_PORT}/"
    )
    connection = await aio_pika.connect_robust(amqp_url)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    print(f"📡 Waiting for messages on queue: {QUEUE_NAME}")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print(f"📥 Received: {message.body.decode()}")