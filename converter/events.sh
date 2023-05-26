echo "Running Converter Async Microservice $HOSTNAME"
gunicorn -b 0.0.0.0:$PORT -w=4 wsgi:app