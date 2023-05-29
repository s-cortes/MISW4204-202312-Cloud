import base64

from events import app
from .consumer import execute_file_conversion
from flask import request, current_app

@app.route('/pubsub/push', methods=['POST'])
def pubsub_push():
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 422

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        payload = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        try:
            task_id = int(payload)
            execute_file_conversion(task_id)
        except Exception as ex:
            return (f"{ex}", 500)

    print(f"receive task {payload}!")

    return ("", 204)

@app.route("/")
def hello_world():
    return "Consumer"
