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

