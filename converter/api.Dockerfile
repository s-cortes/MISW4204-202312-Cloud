FROM python:3

# Setting base file structure
RUN mkdir /backend
RUN mkdir /backend/storage
WORKDIR /backend

# Adding application files
ADD app /backend/app
ADD config /backend/config

# Adding configuration files
ADD api.sh /backend/
ADD app.env /backend/app
ADD db.env /backend/app

# Installing dependencies
ADD api_requirements.txt /backend/
RUN pip install -r api_requirements.txt

ENV FLASK_DEBUG=0
ENV SECRET_KEY=192b9bdd22ab9
ENV UPLOAD_FOLDER="gs://conversion-files-bucket/"

ENV PROJECT_ID="cloud-uniandes"
ENV TOPIC_ID="push-converter"

ENV POSTGRES_PASSWORD="|*`Y6j%Kr3D(p1v["
ENV POSTGRES_USER=scortes
ENV POSTGRES_DB=converter
ENV POSTGRES_NETWORK="35.225.134.183"

EXPOSE 5004
CMD gunicorn -b 0.0.0.0:5004 -w=4 app:app