import os
import enum

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_USER = os.environ.get("POSTGRES_USER")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_NETWORK = os.environ.get("POSTGRES_NETWORK")
SECRET_KEY = os.environ.get("SECRET_KEY")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")

DB_ADDRESS = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_NETWORK}:5432/{DB_NAME}"

print(f"Adress {DB_ADDRESS}")
Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine(DB_ADDRESS)

# reflect the tables
Base.prepare(autoload_with=engine)

# mapped classes are now created with names by default
# matching that of the table name.
User = Base.classes.user
Task = Base.classes.task

class TaskStatus(enum.Enum):
    UPLOADED = "uploaded"
    PROCESSED = "processed"

session = Session(engine)
