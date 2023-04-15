from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
import enum
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Status(enum.Enum):
    UPLOADED = "uploaded"
    PROCESSED = "processed"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(), nullable=False)
    new_format = db.Column(db.String(), nullable=False)
    time_stamp = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    status = db.Column(db.Enum(Status))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def to_dict(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "new_format": self.new_format,
            "time_stamp": self.time_stamp,
            "status": self.status.value,
            "user_id": self.user_id,
        }


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
    time_stamp = fields.DateTime()
    status = fields.String()
    user_id = fields.Integer()

signup_schema = SignUpSchema()
login_schema = LogInSchema()
task_schema = TaskSchema()
