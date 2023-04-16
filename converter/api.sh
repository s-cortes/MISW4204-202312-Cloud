echo "Running Converter Microservice $HOSTNAME"
sleep 7
flask --app app run --host=0.0.0.0 --port=5000
