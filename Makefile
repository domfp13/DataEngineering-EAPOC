# -*- coding: utf-8 -*-
# Created by Luis Enrique Fuentes Plata

SHELL = /bin/bash

.PHONY: create-webapp
create-webapp:
	@ echo "**********Build webapp Docker image based on Dockerfile.webapp**********"
	docker image build --rm -t webapp -f Dockerfile.webapp .
	@ echo "**********Cleaning webapp old webapp image**********"
	docker image prune -f

.PHONY: compose
compose:
	@ echo "**********Standing up services**********"
	docker-compose up

.PHONY: setup
setup: ## Creates and integrates all the services
	@ $(MAKE) create-webapp
	@ $(MAKE) compose

.PHONY: clean
clean: ## Removes running containers
	@ docker-compose down -v --rmi all

.PHONY: run-snowflake
run-snowflake:
	@ echo "Building docker container"
	docker container run -d -p 8080:80 \
		--name my_app -e PORT=80 \
		-e USER= \
		-e PASSWORD= \
		-e ACCOUNT= \
		-e DATABASENAME= \
		-e SCHEMANAME= \
		-e WAREHOUSENAME= \
		-e ROLENAME= \
		webapp:latest

.PHONY: dev
dev:
	@ echo "Building Testing container"
	docker container run -d -p 8080:80 \
		--name my_app \
		--network=ea_poc_dev \
		-e PORT=80 \
		-e POSTGRES_USER=admin \
      	-e POSTGRES_PASSWORD=secret \
      	-e POSTGRES_DB=stage \
		webapp:latest

help:
	@ echo "Please use \`make <target>' where <target> is one of"
	@ perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

