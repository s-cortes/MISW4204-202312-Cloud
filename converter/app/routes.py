from hashlib import md5
from flask import request
from flask_jwt_extended import (
    create_access_token,
    verify_jwt_in_request,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest, UnprocessableEntity

from sqlalchemy import or_
from marshmallow import ValidationError

from app import app
from .models import (
    db,
    signup_schema,
    login_schema,
    task_create_schema,
    task_schema,
    User,
    Task,
    Status,
    ALLOWED_FORMATS,
)


@app.route("/api/auth/signup", methods=["POST"])
def signup():
    try:
        data = signup_schema.load(request.json)
        _validate_signup_data(**data)

        safe_password = md5(data["password1"].encode("utf-8")).hexdigest()
        user = User(
            username=data["username"], email=data["email"], password=safe_password
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully"}, 200
    except ValidationError as err:
        raise BadRequest(
            f"Validation errors on Request Body: {', '.join(err.messages)}"
        )


def _validate_signup_data(username, email, password1, password2):
    """
    Checks whether a new user can be creating using the username, email,
    and passwords given by the request

    Args:
        username (str): The new username
        email (str): The new email
        password1 (str): The new password
        password2 (str): The password confirmation

    Raises:
        UnprocessableEntity: If both passwords do not match
        UnprocessableEntity: If username or email are alredy in use
    """
    if password1 != password2:
        raise UnprocessableEntity("Password mismatch while creating user")

    user = User.query.filter(
        or_(User.username == username, User.email == email)
    ).first()

    if user:
        raise UnprocessableEntity(
            f"A user with username={username} or email={email} already exists"
        )


@app.route("/api/auth/login", methods=["POST"])
def login():
    try:
        data = login_schema.load(request.json)

        safe_password = md5(data["password"].encode("utf-8")).hexdigest()
        user = User.query.filter(
            User.username == data["username"],
            User.password == safe_password,
        ).first()

        if not user:
            raise UnprocessableEntity("Incorrect username and/or password")

        token = create_access_token(identity=user.id)
        return {"access_token": token}, 200
    except ValidationError as err:
        raise BadRequest(
            f"Validation errors on Request Body: {', '.join(err.messages)}"
        )


# def validate_token(auth_token):
#     try:
#         verify_jwt(auth_token, app.config["SECRET_KEY"], algorithms=["HS256"])
#         return True
#     except:
#         return False


@app.route("/api/tasks", methods=["POST"])
@jwt_required()
def create_task():
    try:
        data = task_create_schema.load(request.args)
        user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            raise BadRequest("A file must be included for createing a task")
        file = request.files['file']
        # TODO validar raw_file
        
        task = Task(
            file_name=secure_filename(file.filename),
            old_format="", # TODO obtener el file_format luego de validar
            new_format=data["new_format"],
            status=Status.UPLOADED,
            user_id=user_id,
        )
        db.session.add(task)
        db.session.commit()

        # TODO publish con el task.id dentro del mensaje

        return {"message": "Task created successfully"}, 200
    except ValidationError as err:
        raise BadRequest(
            f"Validation errors on Request Body: {', '.join(err.messages)}"
        )


@app.route("/api/tasks", methods=["GET"])
@jwt_required()
def get_task_list():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        # Get optional query parameters
        max_tasks = request.args.get("max", None, int)
        order = request.args.get("order", None, str)
        # Retrieve tasks for the authenticated user

        task_query = Task.query.filter_by(user_id=user_id)
        # Limit the number of tasks
        if max_tasks:
            task_query = task_query.limit(int(max_tasks))
        # Order the results
        if order == "0":
            task_query = task_query.order_by(Task.id.asc())
        elif order == "1":
            task_query = task_query.order_by(Task.id.desc())
        
        # Return final list of tasks
        tasks = task_query.all()
        return [task_schema.dump(task) for task in tasks], 200
    except:
        return {"error": "Failed to retrieve tasks"}, 500
