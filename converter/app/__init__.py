import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
import datetime
from config import ENV_CONFIG
from .models import db

DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_USER = os.environ.get("POSTGRES_USER")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_NETWORK = os.environ.get("POSTGRES_NETWORK")
SECRET_KEY = os.environ.get("SECRET_KEY")

DB_ADDRESS = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_NETWORK}:5432/{DB_NAME}"

def create_app(db):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        JWT_SECRET_KEY=SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=DB_ADDRESS,
    )
    debug = app.config.get("DEBUG", 0)
    app.config.from_object(ENV_CONFIG[debug])
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)
    app.config['JWT_SECRET_KEY'] = 'secret-key'


    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app


app = create_app(db)

ma = Marshmallow(app)
jwt = JWTManager(app)


from app import routes, handlers
