#!make
PROJECT_VERSION := $(shell python setup.py --version)

SHELL := /bin/bash
PACKAGE := pyaddepar

.PHONY: help test teamcity doc tag clean pypi

.DEFAULT: help

help:
	@echo "make test"
	@echo "       Build the docker image for testing and run them."
	@echo "make teamcity"
	@echo "       Run tests, build a dependency graph and construct the documentation."
	@echo "make doc"
	@echo "       Construct the documentation."
	@echo "make tag"
	@echo "       Make a tag on Github."
	@echo "make pypi"
	@echo "       Release a new version on Pypi. Call from command line"


test:
	mkdir -p artifacts
	docker-compose -f docker-compose.test.yml build sut
	docker-compose -f docker-compose.test.yml run sut

teamcity: test doc

doc: test
	docker-compose -f docker-compose.test.yml run sut sphinx-build /source artifacts/build

tag: test
	git tag -a ${PROJECT_VERSION} -m "new tag"
	git push --tags

clean:
	docker-compose -f docker-compose.yml down -v --rmi all --remove-orphans
	docker-compose -f docker-compose.test.yml down -v --rmi all --remove-orphans

pypi: tag
	python setup.py sdist
	twine check dist/*
	twine upload dist/*

