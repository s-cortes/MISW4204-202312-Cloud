# MISW4204-202312-Cloud
Repository for the development of the functionalities of the cloud conversion tool project, of the Cloud Software Development course

## Build and Local Deployment

For building the application on a local enviroment, the following steps must be carried out

## Deployment | Docker Compose

```bash
$ # First, clone the repo
$ git clone https://github.com/s-cortes/MISW4204-202312-Cloud.git
$ cd MISW4204-202312-Cloud
$
$ # Define a virtual environment (optional)
$ python3 -m venv venv
$ . venv/bin/activate
$
$ # Use Docker Compose CLI to run microservice
$ docker compose up --build -d converter-api
$ docker compose up --build -d --no-deps converter-async
$
$ # Access the UI in browser: http://127.0.0.1:5000/
$
$ # Remove docker containers, local images, and volumes
$ docker compose down -v --rmi local
$
```

<br />

## Code-base structure

The project has a simple structure, represented as bellow:

```bash
< PROJECT ROOT >
📦MISW4204-202312-Cloud
 ┣-- 📂converter
 ┃   ┣-- 📂app
 ┃   ┃   ┣-- 📜__init__.py
 ┃   ┃   ┣-- 📜handlers.py
 ┃   ┃   ┣-- 📜models.py
 ┃   ┃   ┗ 📜routes.py
 ┃   ┃
 ┃   ┣-- 📂config
 ┃   ┃   ┣-- 📜__init__.py
 ┃   ┃   ┗ 📜config.py
 ┃   ┃
 ┃   ┣-- 📜api.Dockerfile
 ┃   ┣-- 📜api.sh
 ┃   ┣-- 📜app.env
 ┃   ┗-- 📜requirements.txt
 ┃
 ┣-- 📜.gitignore
 ┣-- 📜LICENSE
 ┣-- 📜README.md
 ┣-- 📜db.env
 ┗-- 📜docker-compose.yaml
```

## Capacity Tests

For executing the capacity test scenarios, we used Apache Benchmark. The following command was used

```bash
ab -n 5 -c 1 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MTY5MzYzMywianRpIjoiNTFlMWRlM2MtODMzYS00OTQwLTk1YWQtYzQ5NWJkNDRhOTY1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjgxNjkzNjMzLCJleHAiOjE2ODE3ODAwMzN9.2Af8xlh_-XzVfwe2eDr20XNAdV4ZPFBWsv9Bhio8kRI' -p "./converter/tests/data.txt" -T "multipart/form-data; boundary=1234567890" -rk -g "./converter/tests/outputs/output.csv" "http://localhost:5001/api/tasks?new_format=zip"

```

Replace the values `n` and `c` for defining the number of requests and the number os concurrent requests. Additional, generating the access token can be done by using the postman collection (link), or using the following command

```bash
# Signup
curl --location 'http://0.0.0.0:5001/api/auth/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "admin",
    "password1": "admin-password",
    "password2": "admin-password",
    "email": "admini@gmail.com"
}'

# Login
curl --location 'http://0.0.0.0:5001/api/auth/login' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MTY5MzYzMywianRpIjoiNTFlMWRlM2MtODMzYS00OTQwLTk1YWQtYzQ5NWJkNDRhOTY1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjgxNjkzNjMzLCJleHAiOjE2ODE3ODAwMzN9.2Af8xlh_-XzVfwe2eDr20XNAdV4ZPFBWsv9Bhio8kRI' \
--header 'Content-Type: application/json' \
--data '{
    "username": "admin",
    "password": "admin-password"
}'
```
