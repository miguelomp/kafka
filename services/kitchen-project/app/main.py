import json
import os
import sys
import traceback
from random import randrange
from time import sleep

import faust

from models.orders import Food, Order, Status
from models.news import News

KAFKA_TOPIC_ORDER = os.getenv('KAFKA_TOPIC_ORDER', 'orders')
KAFKA_TOPIC_NEWS = os.getenv('KAFKA_TOPIC_NEWS', 'news')
KAFKA_SERVER_URL = os.getenv('KAFKA_SERVER_URL', '')

app = faust.App(
    'kitchen',
    broker=KAFKA_SERVER_URL,
    value_serializer='raw',
)

TOPIC_ORDERS = app.topic(KAFKA_TOPIC_ORDER)
TOPIC_NEWS = app.topic(KAFKA_TOPIC_NEWS)


@app.agent(TOPIC_ORDERS)
async def cook(orders):
    async for order in orders:
        await process_order(order)

async def process_order(raw_order: str):
    order = Order(**json.loads(raw_order.decode("utf-8")))
    timeit1 = randrange(1, 5)
    print(f'=='*10)
    print(f'THE COOKING PROCESS WILL TAKE: {timeit1} seconds')
    print(f'{order}')
    print(f'=='*10)
    new_news = News(order=order, message='Kitchen recieved order')

    await TOPIC_NEWS.send(value=new_news.json().encode('utf-8'))

    try:
        if Food.PIZZA in order.foods:
            raise ValueError(f'WHERE OUT OF {Food.PIZZA.name}')

        sleep(timeit1)
    except Exception as e:
        exc_info = sys.exc_info()
        message = f'Something went wrong ||| error ||| \n{"".join(traceback.format_exception(*exc_info))}'
        new_news = News(order=order, message=message)

        await TOPIC_NEWS.send(value=new_news.json().encode('utf-8'))
    else:
        order.status = Status.IS_READY

        new_news = News(order=order, message='Kitchen finished an order')
        await TOPIC_NEWS.send(value=new_news.json().encode('utf-8'))