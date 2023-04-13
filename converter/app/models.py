from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
import enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)

class Status(enum.Enum):
    UPLOADED = "uploaded"
    PROCESSED = "processed"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(), nullable=False)
    new_format = db.Column(db.String(), nullable=False)
    time_stamp = db.Column(db.Date())
    status = db.Column(db.Enum(Status))

class SignUpSchema(Schema):
    email = fields.Email(required=True)
    username = fields.String(
        required=True,
        validate=[validate.Length(
            min=1,
            max=50,
            error=f"Field must have between {min}-{max} characters")
        ]
    )
    password1 = fields.String(
        required=True,
        validate=[validate.Length(
            min=1,
            max=50,
            error=f"Field must have between {min}-{max} characters")
        ]
    )
    password2 = fields.String(
        required=True,
        validate=[validate.Length(
            min=1,
            max=50,
            error=f"Field must have between {min}-{max} characters")
        ]
    )

class LogInSchema(Schema):
    username = fields.String(
        required=True,
        validate=[validate.Length(
            min=1,
            max=50,
            error=f"Field must have between {min}-{max} characters")
        ]
    )
    password = fields.String(
        required=True,
        validate=[validate.Length(
            min=1,
            max=50,
            error=f"Field must have between {min}-{max} characters")
        ]
    )

class TaskSchema(Schema):
    class Meta:
        model = Task
        load_instance = True

    file_name = fields.String()
    new_format = fields.String()
    time_stamp = fields.String()
    status = fields.String()



signup_schema = SignUpSchema()
login_schema = LogInSchema()
task_schema = TaskSchema()
