import os
from hashlib import md5

from flask import request
from flask import send_from_directory
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest, UnprocessableEntity

from sqlalchemy import or_
from marshmallow import ValidationError

from app import app, publish_file_to_convert, STORAGE_DIR
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


@app.route("/api/tasks", methods=["POST"])
@jwt_required()
def create_task():
    try:
        app.logger.info("Processing upload file")
        data = task_create_schema.load(request.args)
        user_id = get_jwt_identity()

        if "file" not in request.files:
            raise BadRequest("A file must be included for createing a task")

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        file = request.files["file"]
        if file.filename == "":
            raise BadRequest("File cannot be empty")

        new_format = allowed_format(data["new_format"])

        file_name = secure_filename(file.filename)
        file_name_split = file_name.split(".")

        task = Task(
            file_name=file_name_split[0],
            old_format=file_name_split[1],
            new_format=new_format,
            status=Status.UPLOADED.value,
            user_id=user_id,
        )
        db.session.add(task)
        db.session.commit()

        task.file_name = f"{task.file_name}_{task.id}"
        db.session.commit()

        file.save(os.path.join(STORAGE_DIR, file_name))
        publish_file_to_convert(str(task.id))

        response = dict(
            message="Task created successfully",
            filename=task.file_name
        )

        return response, 200
    except ValidationError as err:
        raise BadRequest(
            f"Validation errors on Request Body: {', '.join(err.messages)}"
        )


def allowed_format(compression_type: str):
    """
    This function checks the compression type is allowed for processing

    Args:
        compression_type (str): The compression file type

    Raises:
        UnprocessableEntity: If the compression type is not allowed

    Returns:
        str: The allowed compression type
    """
    if compression_type not in ALLOWED_FORMATS:
        raise UnprocessableEntity("Compress format not allowed")
    return compression_type.lower()


@app.route("/api/tasks", methods=["GET"])
@jwt_required()
def get_task_list():
    try:
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

@jwt_required()
@app.route("/api/files/<filename>", methods=["GET"])
def recovery(filename):
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        task = Task.query.filter(Task.user_id == user_id, Task.file_name == filename).first()
        convertido_type = request.args.get("convertido", None, str)
        if convertido_type == "1":
            if(task.status == Status.PROCESSED.value):
                filename = f"{task.filename}.{task.new_format}"
                return send_from_directory(directory= app.config["UPLOAD_FOLDER"] ,filename=filename)
            else:
                raise BadRequest("Error: File not processed yet")
        elif convertido_type == "0":
            filename = f"{task.filename}.{task.old_format}"
            return send_from_directory(directory= app.config["UPLOAD_FOLDER"] ,filename=filename)
        else:
            raise BadRequest("data/convertido Error: not compatible")
    except:
        return {"error": "Failed to retrieve file"}, 500

@app.route("/api/task/<int:id_task>", methods=["DELETE"])
@jwt_required()
def delete(id_task):
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        task = Task.query.get(id_task)
        filename = f"{task.filename}.{task.new_format}"
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filename = f"{task.filename}.{task.old_format}"
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.delete(task)
        db.session.commit()
        return "Task and Files deleted", 200
    except:
        return {"error": "Failed to delete"}, 500
        
@app.route("/api/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        # Retrieve the task by id and user_id
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return {"error": "Task not found or unauthorized access"}, 404
        return {"task": task.to_dict()}, 200
    except:
        return {"error": "Failed to retrieve task"}, 500
