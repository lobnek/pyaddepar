#!make
PROJECT_VERSION := $(shell python setup.py --version)

SHELL := /bin/bash

.PHONY: help build test doc tag


.DEFAULT: help

help:
	@echo "make build"
	@echo "       Build the docker image."
	@echo "make test"
	@echo "       Build the docker image for testing and run them."
	@echo "make doc"
	@echo "       Construct the documentation."
	@echo "make tag"
	@echo "       Make a tag on Github."

build:
	docker-compose build addepar

test:
	mkdir -p artifacts
	docker-compose -f docker-compose.test.yml build sut
	docker-compose -f docker-compose.test.yml run sut

doc: test
	docker-compose -f docker-compose.test.yml run sut sphinx-build /source artifacts/build

tag: test
	git tag -a ${PROJECT_VERSION} -m "new tag"
	git push --tags

