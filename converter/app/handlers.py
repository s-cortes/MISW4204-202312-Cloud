from werkzeug.exceptions import BadRequest, UnprocessableEntity
from json import dumps
from app import app

@app.errorhandler(BadRequest)
def handle_bad_request(error: BadRequest):
    response = error.get_response()
    response.data = dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description,
    })
    response.content_type = "application/json"
    return response

@app.errorhandler(UnprocessableEntity)
def handle_unprocessable_entity(error):
    response = error.get_response()
    response.data = dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description,
    })
    response.content_type = "application/json"
    return response
