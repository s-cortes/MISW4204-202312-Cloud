import os
import pika

from sqlalchemy.orm.exc import NoResultFound

from .models import session, Task, TaskStatus
from .converter import CustomFileConverterFactory

EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME")
QUEUE_NAME = os.environ.get("ROUTING_QUEUE")
KEY_NAME = os.environ.get("ROUTING_KEY_NAME")

STORAGE_DIR = os.environ.get("STORAGE_DIR")

connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()

channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct")

result = channel.queue_declare(queue=QUEUE_NAME, exclusive=False)
queue_name = result.method.queue

channel.queue_bind(
    exchange=EXCHANGE_NAME, queue=queue_name, routing_key=KEY_NAME
)

def execute_file_conversion(ch, method, properties, body):
    task_id = int(body.decode("utf-8"))
    task = session.query(Task).filter_by(id=task_id).first()

    try:
        if not task:
            raise NoResultFound()
        
        decompressed_path = os.path.join(STORAGE_DIR, task.file_name)

        # Decompresses the file. It is necessary that de decompression doesn't affect
        # the current directory, so a new directory has to be created with the name of the
        # task.file_name
        decompressor = CustomFileConverterFactory.get_custom_file_converter(task.old_format)
        decompressor.decompress_file(input_path=task.file_name, output_path=decompressed_path)

        # Once it's decompressed, the compression to the new format can be done using
        # the previously created directoy from task.file_name
        compressor = CustomFileConverterFactory.get_custom_file_converter(task.new_format)
        compressor.compress_file(input_path=decompressed_path, output_path=STORAGE_DIR)

        task.status = TaskStatus.PROCESSED
        session.commit()
    except NoResultFound as rnf_ex:
        print(rnf_ex)
    except Exception as ex:
        print(ex)


channel.basic_consume(
    queue=queue_name, on_message_callback=execute_file_conversion, auto_ack=True
)
channel.start_consuming()
