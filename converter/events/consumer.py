import os
import datetime
import pika

from sqlalchemy.orm.exc import NoResultFound

from .models import session, Task, TaskStatus
from .converter import CustomFileCompressorFactory

from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from google.cloud import storage


path_to_private_key = os.environ.get("KEY_PATH")

client = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)

bucket = storage.Bucket(client, 'conversion-files-bucket')

timeout = 10.0
EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME")
QUEUE_NAME = os.environ.get("ROUTING_QUEUE")
KEY_NAME = os.environ.get("ROUTING_KEY_NAME")
PROJECT_ID = os.environ.get("PROJECT_ID")
SUBSCRIPTION = os.environ.get("SUBSCRIPTION")


def execute_file_conversion(task_id:int):
    status = TaskStatus.PROCESSED.value
    print(f"MQ - Consuming new message from queue (body={task_id})")

    try:
        task = session.query(Task).filter_by(id=task_id).first()
        if not task:
            raise NoResultFound()
        task.processed_ts = datetime.datetime.utcnow()
        compressor = CustomFileCompressorFactory.get_custom_file_converter(
            task.new_format
        )

        # Get the file from Cloud Storage
        blob = bucket.blob(task.file_name)
        file_data = blob.download_as_bytes()

        # Call compress_file method with a file object instead of a path
        compressor.compress_file(
            file=file_data,
            file_name=task.file_name,
            old_format=task.old_format
        )

    except NoResultFound as rnf_ex:
        status = TaskStatus.FAILED.value
        print(f"MQ - Processing Task Not Found on BD: {rnf_ex}")
    except Exception as ex:
        status = TaskStatus.FAILED.value
        print(f"MQ - Encountered Error while processing message: {ex}")
    finally:
        try:
            task.status = status
            session.commit()
        except Exception as ferr:
            print(f"MQ - Encountered Error while finalizing message: {ferr}")

        print("MQ - Completed message processing") 


def gcp_callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    task_id = int(message.data.decode("utf-8"))
    execute_file_conversion(task_id)
    message.ack()


def rabbit_calback(ch, method, properties, body):
    """
    Callback function for processing async compression requests.

    Args:
        ch (BlockingChannel): Connection channel
        method (any): method
        properties (any): properties
        body (any): Message, contains the task id for processing

    Raises:
        NoResultFound: If the task id cannot retrive a row from DB
    """

    task_id = int(body.decode("utf-8"))
    execute_file_conversion(task_id)


def rabbit_consume():
    print(f"Starting RabbitMQ Subscription to {EXCHANGE_NAME}/{QUEUE_NAME}/{KEY_NAME}")
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq", heartbeat=600)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct")

    result = channel.queue_declare(queue=QUEUE_NAME, exclusive=False)
    queue_name = result.method.queue

    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=KEY_NAME)

    channel.basic_consume(
    queue=queue_name, on_message_callback=rabbit_calback, auto_ack=True
    )
    channel.start_consuming()


def gcp_consumer():
    print(f"Starting GCP-Pub/Sub..")
    GCPSUSCRIBE = pubsub_v1.SubscriberClient()
    subscription_path = GCPSUSCRIBE.subscription_path(PROJECT_ID, SUBSCRIPTION)
    streaming_pull_future = GCPSUSCRIBE.subscribe(subscription_path, callback=gcp_callback)
    print(f"Listening GCP-Pub/Sub for messages on {subscription_path}..\n")

    with GCPSUSCRIBE:
        try:
            #streaming_pull_future.result(timeout=timeout)
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()


debug = os.environ.get("EVENTS_DEBUG", 0) == 1
print(f"debug:{debug}")
if (debug):
    rabbit_consume()
else:
    gcp_consumer()
