all: generate run

generate:
	@echo "Building docker image"
	docker image build --rm -t webapp .

run:
	@echo "Building docker container"
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
	docker rmi $(docker images -a|grep "<none>"|awk '$1=="<none>" {print $3}')