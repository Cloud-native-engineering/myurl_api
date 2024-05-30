# Base python package
FROM python:3.10.0-alpine

# Working directory
WORKDIR /app

# Copy the dependencies
COPY requirements.txt requirements.txt

# Install requirements & install Gunicorn  
RUN pip install -r requirements.txt && pip install gunicorn==21.2

# for flask web server
EXPOSE 5000

# add files
ADD . /app

# This is the runtime command for the container
# Add below line if not using docker-compose
CMD gunicorn --preload -w 1 -b 0.0.0.0:5000 wsgi:app
