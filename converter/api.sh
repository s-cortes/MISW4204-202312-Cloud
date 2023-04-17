echo "Running Converter API Microservice $HOSTNAME"
sleep 10
gunicorn -b 0.0.0.0:5000 -w=4 wsgi:app
