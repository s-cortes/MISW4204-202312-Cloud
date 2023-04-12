FROM python:3
RUN mkdir /backend
WORKDIR /backend
ADD api.sh /backend/

ADD requirements.txt /backend/
RUN pip install -r requirements.txt

ADD app /backend/app
ADD config /backend/config
EXPOSE 8080
