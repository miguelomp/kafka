import json
import os

import faust

from models.news import News
from models.orders import Status

KAFKA_TOPIC_NEWS = os.getenv('KAFKA_TOPIC_NEWS', 'news')
KAFKA_SERVER_URL = os.getenv('KAFKA_SERVER_URL', '')

app = faust.App(
    'announcement',
    broker=KAFKA_SERVER_URL,
    value_serializer='raw',
)

TOPIC_NEWS = app.topic(KAFKA_TOPIC_NEWS)

@app.agent(TOPIC_NEWS)
async def announce(news):
    async for new_raw in news:
        new_news = News(**json.loads(new_raw.decode("utf-8")))
        if new_news.order.status is Status.IS_READY:
            print(new_news)
        elif 'error' in new_news.message:
            print(new_news.message)
        else:
            print('not useful news arrived')
        
        