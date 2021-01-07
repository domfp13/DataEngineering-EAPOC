SHELL = /bin/bash

all: generate run

.PHONY: remove
remove:
	@ echo "Removing container"
	@ docker container stop my_app && docker container rm my_app

.PHONY: generate
generate:
	@ echo "Building docker image"
	docker image build --rm -t webapp .

.PHONY: run
run:
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

.PHONY: clean
clean:
	@echo "Cleaning up..."
	docker image prune -f

.PHONY: refactor
refactor: remove generate clean run