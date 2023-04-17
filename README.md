# MISW4204-202312-Cloud
Repository for the development of the functionalities of the cloud conversion tool project, of the Cloud Software Development course

## Useful links

* [Postman Collection](https://app.getpostman.com/join-team?invite_code=cae57394629ace32d62eb6ae4f54096a&target_code=5cc4486c5f15defe8321bd338038b6af)
* [Reporte Pruebas de Estrés](https://uniandes-my.sharepoint.com/:b:/g/personal/l_simonetti_uniandes_edu_co/EUTwOnjRYWZKmzqXi2xhOC4Bc2kx2h1KGPqGV-zhcODzpQ?e=XrMCNC)
* [Video Sustentación](https://uniandes-my.sharepoint.com/:f:/g/personal/l_simonetti_uniandes_edu_co/EiAFKYbMZ4hAt3ECM4rZFn0BL8coWWLTMnKXGFa4d7tx1A?e=cqaxm6)

## Code-base structure

The project has a simple structure, represented as bellow:

```bash
< PROJECT ROOT >
📦MISW4204-202312-Cloud
 ┣-- 📂converter
 ┣-- 📂app
 ┃   ┃   ┣-- 📜__init__.py
 ┃   ┃   ┣-- 📜handlers.py
 ┃   ┃   ┣-- 📜models.py
 ┃   ┃   ┗-- 📜routes.py
 ┃   ┃
 ┃   ┣-- 📂config
 ┃   ┃   ┣ 📜__init__.py
 ┃   ┃   ┗ 📜config.py
 ┃   ┃
 ┃   ┣-- 📂events
 ┃   ┃   ┣-- 📜__init__.py
 ┃   ┃   ┣-- 📜consumer.py
 ┃   ┃   ┣ 📜converter.py
 ┃   ┃   ┗-- 📜models.py
 ┃   ┃
 ┃   ┣-- 📂tests
 ┃   ┃   ┣-- 📂outputs
 ┃   ┃   ┃
 ┃   ┃   ┣-- 📜data.txt
 ┃   ┃   ┗-- 📜test_file.jpg
 ┃   ┃
 ┃   ┣-- 📜api.Dockerfile
 ┃   ┣-- 📜api.sh
 ┃   ┣-- 📜api_requirements.txt
 ┃   ┣-- 📜app.env
 ┃   ┣-- 📜events.Dockerfile
 ┃   ┣-- 📜events.env
 ┃   ┣-- 📜events.sh
 ┃   ┣-- 📜events_requirements.txt
 ┃   ┗-- 📜wsgi.py
 ┃
 ┣-- 📜.gitignore
 ┣-- 📜LICENSE
 ┣-- 📜README.md
 ┣-- 📜db.env
 ┗-- 📜docker-compose.yaml
```

## Arquitectura

![4204-arquitectura drawio](https://user-images.githubusercontent.com/25346635/232369165-2d758a07-35d2-44be-a746-9ff9cd297835.png)

<br />

## Build & Deployment | Docker Compose

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

For executing the capacity test scenarios, we used Apache Benchmark. The following commands were used

```bash
# Install Apache Bencmark and graphing tool
sudo apt install apache2-utils
sudo apt-get install gnuplot

# Execute test | replace <token>
ab -n 1000 -c 10 -H 'Authorization: Bearer <token>' -p "./converter/tests/data.txt" -T "multipart/form-data; boundary=1234567890" -rk -g "./converter/tests/outputs/output.csv" "http://0.0.0.0:5001/api/tasks?new_format=zip"

# Graph results
gnuplot plot.p
```

Replace the values `n` and `c` for defining the number of requests and the number os concurrent requests. Additional, generating the access token can be done by using the postman collection (link), or using the following command.

Regarding the graph generation tool, create a file `plot.p` with the following data

```text
set terminal png size 600
set output "output.png"
set title "XX Requests, YY Concurrent Requests"
set size ratio 0.6
set grid y
set xlabel "Num. Requests"
set ylabel "Response Time (ms)"
plot "output.csv" using 9 smooth sbezier with lines title "http://ip_servidor/cipher"

```

### Capacity Test Results

The results from each of the defined scenarios can be found on the following link
