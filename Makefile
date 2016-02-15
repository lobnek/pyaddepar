# Makefile
#

ROOT_DIR      = $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON        = ${ROOT_DIR}/env/bin/python

PROJECT       = pyaddepar

.PHONY: all
all:
	@$(MAKE) build


.PHONY: clean
clean:
	rm -rf ${ROOT_DIR}/env


.PHONY: build
build:
	@$(MAKE) clean
	conda create --yes -p ${ROOT_DIR}/env --file condalist.txt


.PHONY: tag
tag:
	git tag -a $(VERSION) -m 'version $(VERSION)'
	git push --tags

