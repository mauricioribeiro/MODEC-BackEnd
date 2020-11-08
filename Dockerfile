FROM python:3.7.9-alpine3.12
LABEL Author=mauricioribeiro1992@gmail.com

# Exposing container HTTP port
EXPOSE 8000

# Setting up api folder
RUN mkdir -p /modec
ADD . /modec
WORKDIR /modec

# Install api dependencies
RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev
RUN pip install -r requirements.txt

# Apply migrations, run unittests and start api
ENTRYPOINT python manage.py migrate && \
           python manage.py test && \
           python manage.py runserver 0.0.0.0:8000 --noreload