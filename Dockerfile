############################################################
# Dockerfile to build Flask App
# Based on
############################################################

# Set the base image
FROM debian:latest

# File Author / Maintainer
MAINTAINER Sagar
#RUN apt-get update && apt-get install -y gnupg2
#COPY ./nginx_signing.key /var/www/app/nginx_signing.key
#RUN apt-key add /var/www/app/nginx_signing.key
#RUN echo "deb http://nginx.org/packages/debian/ jessie nginx" >> /etc/apt/sources.list
#RUN echo "deb-src http://nginx.org/packages/debian/ jessie nginx" >> /etc/apt/sources.list
#RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN apt-get update && apt-get install -y nginx \
    build-essential \
    python3 \
    python3-dev\
    python3-pip \
    default-libmysqlclient-dev \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*
RUN pip3 install uwsgi -I
 # Copy over and install the requirements
COPY ./app/requirements.txt /var/www/app/app/requirements.txt
RUN pip3 install -r /var/www/app/app/requirements.txt

COPY ./run.py ./uwsgi.ini ./app.conf /var/www/app/
RUN  ln -s /var/www/app/app.conf /etc/nginx/conf.d/
COPY ./app /var/www/app/app/

WORKDIR /var/www/app

EXPOSE 80

CMD ["/bin/bash", "-c", "nginx; uwsgi uwsgi.ini"]

