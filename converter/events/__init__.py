import os

from flask import Flask
from google.cloud import pubsub_v1

app = Flask(__name__, instance_relative_config=True)
debug = app.config.get("DEBUG", 0)

# Configure the following environment variables via app.yaml
# This is used in the push request handler to verify that the request came from
# pubsub and originated from a trusted source.
app.config['PUBSUB_TOPIC'] = os.environ.get('PUBSUB_TOPIC')
app.config['PROJECT'] = os.environ.get('PROJECT_ID')
app.config['PUBSUB_VERIFICATION_TOKEN'] = \
    os.environ.get('PUBSUB_VERIFICATION_TOKEN')

from events import routes

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5001)