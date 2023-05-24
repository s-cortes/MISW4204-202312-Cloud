import os
import pika

from google.cloud import pubsub_v1

GCPPUBLISHER = pubsub_v1.PublisherClient()
EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME")
KEY_NAME = os.environ.get("ROUTING_KEY_NAME")
PROJECT_ID = os.environ.get("PROJECT_ID")
TOPIC_ID = os.environ.get("TOPIC_ID")

class Publisher:
    def gcp_publisher(message: str):
        topic_path = GCPPUBLISHER.topic_path(PROJECT_ID, TOPIC_ID)
        message = message.encode("utf-8")
        GCPPUBLISHER.publish(topic_path, data=message)

    def rabbit_publisher(message: str):

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq", heartbeat=600)
        )
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct")

        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=KEY_NAME, body=message)
        connection.close()
