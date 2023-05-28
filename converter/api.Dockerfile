FROM python:3

# Setting base file structure
RUN mkdir /backend
RUN mkdir /backend/storage
WORKDIR /backend


# Adding configuration files
ADD api.sh /backend/
ADD app.env /backend/
ADD db.env /backend/

# Adding application files
ADD app /backend/app
ADD wsgi.py /backend/
ADD config /backend/config

# Installing dependencies
ADD api_requirements.txt /backend/
RUN pip install -r api_requirements.txt


EXPOSE 5000
CMD sh api.sh