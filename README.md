# MISW4204-202312-Cloud
Repository for the development of the functionalities of the cloud conversion tool project, of the Cloud Software Development course

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

<br />

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

## Interfaces

For testing the api, it is possible to use the following Postman Collection ([link](https://app.getpostman.com/join-team?invite_code=cae57394629ace32d62eb6ae4f54096a&target_code=5cc4486c5f15defe8321bd338038b6af)). Additional, the endpoints can be also reached using the following cURLs

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
--header 'Content-Type: application/json' \
--data '{
    "username": "admin",
    "password": "admin-password"
}'

# Create Compression Task | Replace <token>
curl --location 'http://0.0.0.0:5001/api/tasks' \
--header 'Authorization: Bearer <token>'

# Get Tasks | Replace <token>
curl --location 'http://0.0.0.0:5001/api/tasks?max=1000&order=1' \
--header 'Authorization: Bearer <token>'

# Get Task | Replace <token>
curl --location 'http://0.0.0.0:5001/api/tasks/<id_task>' \
--header 'Authorization: Bearer <token>'

# Delete Task | Replace <token> and <id_task>
curl --location --request DELETE 'http://0.0.0.0:5001/api/tasks/<id_task>' \
--header 'Authorization: Bearer <token>'

# Get File | Replace <token> adn <file_name>
curl --location 'http://0.0.0.0:5001/api/files/<file_name>?convertido=0' \
--header 'Authorization: Bearer <token>'
```

<br />

## Capacity Tests

For executing the capacity test scenarios, we used Apache Benchmark. The following command was used

```bash
ab -n 100 -c 10 -H 'Authorization: Bearer <token>' -p "./converter/tests/data.txt" -T "multipart/form-data; boundary=1234567890" -rk -g "./converter/tests/outputs/output.csv" "http://localhost:5001/api/tasks?new_format=zip"

```

Replace the values `n` and `c` for defining the number of requests and the number os concurrent requests. Additional, generating the access token can be done by using the postman collection (link), or using the following command


