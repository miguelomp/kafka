import json
import os

import faust

KAFKA_TOPIC_NEWS = os.getenv('KAFKA_TOPIC_NEWS', 'news')
KAFKA_SERVER_URL = os.getenv('KAFKA_SERVER_URL', '')

app = faust.App(
    'announcement',
    broker=KAFKA_SERVER_URL,
    value_serializer='raw',
)

news_topic = app.topic(KAFKA_TOPIC_NEWS)

@app.agent(news_topic)
async def announce(news):
    async for new in news:
        order_details = json.loads(new.decode("utf-8"))
        print(order_details)
        