echo "Running Converter API Microservice $HOSTNAME"
sleep 10
# flask --app app run --host=0.0.0.0 --port=5000
gunicorn -b 0.0.0.0:5000 -w=2 wsgi:app
