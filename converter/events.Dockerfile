FROM python:3

# Setting base file structure
RUN mkdir /backend
RUN mkdir /backend/storage
WORKDIR /backend

ADD events.sh /backend/
ADD events /backend/events


# Adding configuration files
ADD api.sh /backend/
ADD events.env /backend/events
ADD db.env /backend/events

# Adding application files
ADD events /backend/events

# Installing dependencies
ADD events_requirements.txt /backend/
RUN pip install -r events_requirements.txt

ENV EVENTS_DEBUG=0
ENV EXCHANGE_NAME="converter_exchange_name"
ENV ROUTING_KEY_NAME="converter_request_key"
ENV ROUTING_QUEUE="converter_queue"

ENV PROJECT_ID="cloud-uniandes"
ENV TOPIC_ID="push-converter"
ENV SUBSCRIPTION="push-converter-sub"

ENV POSTGRES_PASSWORD="|*`Y6j%Kr3D(p1v["
ENV POSTGRES_USER=scortes
ENV POSTGRES_DB=converter
ENV POSTGRES_NETWORK="35.225.134.183"

EXPOSE 5004
CMD gunicorn -b 0.0.0.0:5004 -w=4 events:app