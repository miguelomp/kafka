import json
import os
import sys
import traceback
from random import randrange
from time import sleep, time
import datetime

import faust

KAFKA_TOPIC_ORDER = os.getenv('KAFKA_TOPIC_ORDER', 'orders')
KAFKA_TOPIC_NEWS = os.getenv('KAFKA_TOPIC_NEWS', 'news')
KAFKA_SERVER_URL = os.getenv('KAFKA_SERVER_URL', '')

app = faust.App(
    'kitchen',
    broker=KAFKA_SERVER_URL,
    value_serializer='raw',
)

orders_topic = app.topic(KAFKA_TOPIC_ORDER)
news_topic = app.topic(KAFKA_TOPIC_NEWS)


@app.agent(orders_topic)
async def cook(orders):
    async for order in orders:
        print(order)
        timeit0 = randrange(0, 2)
        timeit1 = randrange(1, 5)
        try:
            # from the api the order come as {'item': i, 'price': randint(100, 250)}
            order_json = json.loads(order.decode("utf-8"))
            data = {
                "message": f"started order {order}",
                "at": str ( datetime.datetime.now() ),
                "order": order_json
            }
            ini_log = json.dumps(data).encode("utf-8")
            await news_topic.send(value=ini_log)

            sleep(timeit0)
            # force an error
            if order_json['item'] == '🥐':
                raise ValueError(f'WHERE OUT OF {order_json["item"]}')
            else:
                print(f'cooking f{order_json["item"]}')
            sleep(timeit1)

            pass
        except Exception as e:
            exc_info = sys.exc_info()
            data = {
                "message": f"error on order {order}, the kitchen is in fire!",
                "at": str ( datetime.datetime.now() ),
                "error": ''.join(traceback.format_exception(*exc_info)),
                "order": order_json
            }
            ini_log = json.dumps(data).encode("utf-8")
            await news_topic.send(value=ini_log)
            pass
        else:
            data = {
            "message": f"finished order {order} ready to deliver",
            "at": str ( datetime.datetime.now() ),
            "order": order_json
            }
            ini_log = json.dumps(data).encode("utf-8")
            await news_topic.send(value=ini_log)
            pass
