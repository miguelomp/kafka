
from kafka import KafkaProducer

from .configs import KAFKA_SERVER_URL, KAFKA_TOPIC_ORDER
from .models.orders import Order, Status

TOPIC_KITCHEN = KafkaProducer(bootstrap_servers=KAFKA_SERVER_URL)

async def send_to_kitchen(order: Order):
    order.status = Status.ORDERED
    print(order.json())
    TOPIC_KITCHEN.send(topic=KAFKA_TOPIC_ORDER, value=order.json().encode('utf-8'))
