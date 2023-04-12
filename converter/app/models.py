from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)



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

signup_schema = SignUpSchema()
login_schema = LogInSchema()