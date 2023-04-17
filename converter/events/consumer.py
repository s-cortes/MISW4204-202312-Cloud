import os
import datetime
import pika

from sqlalchemy.orm.exc import NoResultFound

from .models import session, Task, TaskStatus
from .converter import CustomFileCompressorFactory

EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME")
QUEUE_NAME = os.environ.get("ROUTING_QUEUE")
KEY_NAME = os.environ.get("ROUTING_KEY_NAME")

STORAGE_DIR = os.environ.get("STORAGE_DIR")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq", heartbeat=600)
)
channel = connection.channel()
print(f"Starting Subscription to {EXCHANGE_NAME}/{QUEUE_NAME}/{KEY_NAME}")

channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct")

result = channel.queue_declare(queue=QUEUE_NAME, exclusive=False)
queue_name = result.method.queue

channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=KEY_NAME)


def execute_file_conversion(ch, method, properties, body):
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
    status = TaskStatus.PROCESSED.value
    print(f"MQ - Consuming new message from queue (body={task_id})")

    try:
        task = session.query(Task).filter_by(id=task_id).first()
        if not task:
            raise NoResultFound()

        compressor = CustomFileCompressorFactory.get_custom_file_converter(
            task.new_format
        )
        compressor.compress_file(
            path=STORAGE_DIR, file_name=task.file_name, old_format=task.old_format
        )
    except NoResultFound as rnf_ex:
        status = TaskStatus.FAILED.value
        print(f"MQ - Processing Task Not Found on BD: {rnf_ex}")
    except Exception as ex:
        status = TaskStatus.FAILED.value
        print(f"MQ - Encountered Error while processing message: {ex}")
    finally:
        task.status = status
        task.processed_ts = datetime.datetime.utcnow()
        session.commit()
        print("MQ - Completed message processing") 


channel.basic_consume(
    queue=queue_name, on_message_callback=execute_file_conversion, auto_ack=True
)
channel.start_consuming()
