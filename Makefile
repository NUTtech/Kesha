.PHONY:
	help
	lock-deps
	shell
	autotests
	lint
	build
	envfile
	runserver
	runserver-uvicorn

.DEFAULT_GOAL := help

help:  ## List all commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

OVERRIDE=`test -f deploy/docker-compose.override.yml && \
		  echo '-f deploy/docker-compose.override.yml'`

lock-deps:  ## Make poetry.lock
	docker-compose \
		-f deploy/docker-compose.yml \
		-f deploy/docker-compose.develop.yml \
		${OVERRIDE} \
		--project-directory . \
		run --rm parrot-app poetry lock

shell:  ## Shell (bash) intro the app's container
	docker-compose \
		-f deploy/docker-compose.yml \
		-f deploy/docker-compose.db.yml \
		-f deploy/docker-compose.develop.yml \
		${OVERRIDE} \
		--project-directory . \
		run --rm parrot-app bash

autotests:  ## Start project's tests on docker
	docker-compose \
		-f deploy/docker-compose.yml \
		-f deploy/docker-compose.db.yml \
		-f deploy/docker-compose.autotests.yml \
		${OVERRIDE} \
		--project-directory . \
		run --rm parrot-app-tests

lint:  ## Start project's lint on docker
	docker-compose \
	    -f deploy/docker-compose.yml \
	    ${OVERRIDE} \
	    --project-directory . \
	    run --rm parrot-app \
	        flake8 --count

build:  ## Build docker image
	docker-compose \
		-f deploy/docker-compose.yml \
		${OVERRIDE} \
		--project-directory . \
		build parrot-app

envfile:  ## Generate env file with variables with prefix PARROT_
	env | egrep ^PARROT_ > .gen.env

runserver:  envfile  ## Local startup the app on docker with required services
	docker-compose \
		-f deploy/docker-compose.yml \
		-f deploy/docker-compose.db.yml \
		-f deploy/docker-compose.develop.yml \
		${OVERRIDE} \
		--project-directory . \
		up

runserver-uvicorn:  envfile  ## Local startup the app on docker with uvicorn
	docker-compose \
		-f deploy/docker-compose.yml \
		-f deploy/docker-compose.db.yml \
		${OVERRIDE} \
		--project-directory . \
		up
