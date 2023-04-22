import os
import pika

from app import app
from google.cloud import pubsub_v1




GCPPUBLISHER = pubsub_v1.PublisherClient()
EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME")
KEY_NAME = os.environ.get("ROUTING_KEY_NAME")


def gcp_publisher(message: str):
    app.logger.info(f"Starting GCP PUB/SUB Connection")
    topic_path = GCPPUBLISHER.topic_path("cloud-uniandes", "converter")
    GCPPUBLISHER.publish(topic_path, message)

def rabbit_publisher(message: str):
    app.logger.info(f"MQ - Starting RabbitMQ Connection")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq", heartbeat=600)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct")

    app.logger.info(f"MQ - Basic Publish with message={message}")
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=KEY_NAME, body=message)
    connection.close()
    app.logger.info(f"MQ - Completed Basic Publish successfully")
