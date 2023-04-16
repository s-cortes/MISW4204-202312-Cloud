import os
import pika

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from config import ENV_CONFIG
from .models import db

DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_USER = os.environ.get("POSTGRES_USER")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_NETWORK = os.environ.get("POSTGRES_NETWORK")
SECRET_KEY = os.environ.get("SECRET_KEY")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")

DB_ADDRESS = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_NETWORK}:5432/{DB_NAME}"
#DB_ADDRESS = f"postgresql://postgres:password@localhost:5432/flasksql2"

EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME")
KEY_NAME = os.environ.get("ROUTING_KEY_NAME")

STORAGE_DIR = os.environ.get("STORAGE_DIR")


def publish_file_to_convert(message: str):
    """_summary_

    Args:
        message (str): _description_
    """
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


def create_app(db):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        JWT_SECRET_KEY=SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=DB_ADDRESS,
        UPLOAD_FOLDER=UPLOAD_FOLDER,
    )
    debug = app.config.get("DEBUG", 0)
    app.config.from_object(ENV_CONFIG[debug])

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app


app = create_app(db)

ma = Marshmallow(app)
jwt = JWTManager(app)


from app import routes, handlers
