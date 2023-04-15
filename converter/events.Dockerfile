FROM python:3

RUN mkdir /backend
RUN mkdir /backend/storage
WORKDIR /backend

ADD events.sh /backend/
ADD events /backend/
ADD events_requirements.txt /backend/

RUN pip install -r events_requirements.txt
