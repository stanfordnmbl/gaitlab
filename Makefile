.PHONY: docker
docker:
	docker build . -t stanfordnmbl/gaitlab

.PHONY: push
push:
	docker build . -t stanfordnmbl/gaitlab

.PHONY: run
run:
	docker rm gaitlab 2> /dev/null
	docker-compose up

