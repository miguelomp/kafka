import os

ROUTE_ORDERS='/orders'

KAFKA_TOPIC_ORDER = os.getenv('KAFKA_TOPIC_ORDER', 'orders')
KAFKA_SERVER_URL = os.getenv('KAFKA_SERVER_URL', '')

if not len(KAFKA_SERVER_URL):
    raise ConnectionError('KAFKA_SERVER_URL not set')