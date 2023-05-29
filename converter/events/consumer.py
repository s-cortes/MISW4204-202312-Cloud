import os
import datetime
import pika

from sqlalchemy.orm.exc import NoResultFound

from .models import session, Task, TaskStatus
from .converter import CustomFileCompressorFactory

from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from google.cloud import storage


client = storage.Client()
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
        blob = bucket.blob(f"{task.file_name}.{task.old_format}")
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

debug = os.environ.get("EVENTS_DEBUG", 0) == 1
print(f"debug:{debug}")