# -*- coding: utf-8 -*-
# Copyright (c) CompuCom, All Rights Reserved

# Python image to use.
FROM python:3.7-slim

# Set the working directory to /app
ENV APP_HOME /app
WORKDIR $APP_HOME

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app 
WORKDIR $APP_HOME
COPY . .

#RUN pip install Flask gunicorn flask-wtf snowflake-sqlalchemy

# Run app.py when the container launches
CMD exec gunicorn --bind :$PORT app:app