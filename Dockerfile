FROM python:3.9

# File Author / Maintainer
MAINTAINER Sagar

# Copy the requirements file
COPY ./app/requirements.txt /var/www/app/app/requirements.txt


# Install the required packages
#RUN pip3 install -r /var/www/app/app/requirements.txt
RUN pip3 install --no-cache-dir -r /var/www/app/app/requirements.txt gunicorn

# Copy the application code
COPY ./app /var/www/app/app/

# Set the working directory inside the container
WORKDIR /var/www/app

# Expose port 80 and 443
EXPOSE 80
EXPOSE 443

# Start the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--keyfile", "/certs/server.key", "--certfile", "/certs/server.cert", "app:app"]