FROM python:3
RUN mkdir /backend
RUN mkdir /backend/storage
WORKDIR /backend
ADD api.sh /backend/

ADD api_requirements.txt /backend/
RUN pip install -r api_requirements.txt

ADD app /backend/app
ADD config /backend/config
EXPOSE 8080
