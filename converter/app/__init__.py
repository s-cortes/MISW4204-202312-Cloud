import os
import pika

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from config import ENV_CONFIG
from .models import db
from .publisher import Publisher

DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_USER = os.environ.get("POSTGRES_USER")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_ADDRESS = os.environ.get("POSTGRES_NETWORK")

SQLALCHEMY_DB_URI= f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:5432/{DB_NAME}"

SECRET_KEY = os.environ.get("SECRET_KEY")
STORAGE_DIR = os.environ.get("UPLOAD_FOLDER")


EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME")
KEY_NAME = os.environ.get("ROUTING_KEY_NAME")


def publish_file_to_convert(message: str):
    """_summary_

    Args:
        message (str): _description_
    """
    debug = app.config.get("DEBUG", 0)
    if (debug):
        Publisher.rabbit_publisher(message)
    else:
        Publisher.gcp_publisher(message)
    


def create_app(db):
    app = Flask(__name__, instance_relative_config=True)
    debug = app.config.get("DEBUG", 0)

    app.config.from_mapping(
        JWT_SECRET_KEY=SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DB_URI,
        UPLOAD_FOLDER=STORAGE_DIR,
    )
    app.config.from_object(ENV_CONFIG[debug])

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app


app = create_app(db)

ma = Marshmallow(app)
jwt = JWTManager(app)


from app import routes, handlers
