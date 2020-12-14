# -*- coding: utf-8 -*-
# Copyright (c) CompuCom, All Rights Reserved

# Adding official python image
FROM python:3.7-slim

# Copy local code to the container image.
ENV APP_HOME /webapp
WORKDIR $APP_HOME
COPY . ./

#RUN pip install Flask gunicorn 
RUN pip install Flask gunicorn snowflake-sqlalchemy

# Running
CMD exec gunicorn --bind :$PORT app:app