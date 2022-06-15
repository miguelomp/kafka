from operator import le
from typing import List
from fastapi import FastAPI
from kafka import KafkaProducer
from random import randint
import json

import os

KAFKA_TOPIC_ORDER = os.getenv('KAFKA_TOPIC_ORDER', 'orders')
KAFKA_SERVER_URL = os.getenv('KAFKA_SERVER_URL', '')

if not len(KAFKA_SERVER_URL):
    raise ConnectionError('KAFKA_SERVER_URL not set')

app = FastAPI()
kitchen_pool = KafkaProducer(bootstrap_servers=KAFKA_SERVER_URL)


items_prices = { n: {'item': i, 'price': randint(100, 250)} for n, i in enumerate('🍕🍔🍟🌭🍿🧂🥞🧇🥐🥗')}


@app.get("/")
def app_root():
    return {"Hello": "World"}


@app.get("/{order_id}")
def set_order(order_id: int):
    if not 0 <= order_id < 10:
        return {'message': f"The order {order_id} does not exists!"}

    kitchen_pool.send(KAFKA_TOPIC_ORDER, json.dumps(items_prices[order_id]).encode("utf-8"))

    return {'message': f"The order {items_prices[order_id]} is scheduled!\nTotal cost: $ {items_prices[order_id]['price']}"}

@app.post("/orders")
def send_service(orders: List[int]):
    if any(not 0 <= order_id < 10 for order_id in orders):
        return {'message': f"The order {order_id} does not exists!"}
    
    for order_id in orders:
        kitchen_pool.send(KAFKA_TOPIC_ORDER, json.dumps(items_prices[order_id]).encode("utf-8"))

    return {'message': f"The orders {[items_prices[order_id] for order_id in orders]} are scheduled!\nTotal cost: $ {sum([items_prices[order_id]['price'] for order_id in orders])}"}