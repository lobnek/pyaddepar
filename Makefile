# Makefile
#

ROOT_DIR      = $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON        = ${ROOT_DIR}/env/bin/python
NOSE          = ${ROOT_DIR}/env/bin/nosetests

PROJECT       = pyaddepar

.PHONY: all
all:
	@$(MAKE) test
	@$(MAKE) publish


.PHONY: clean
clean:
	rm -rf ${ROOT_DIR}/env


.PHONY: build
build:
	@$(MAKE) clean
	conda create --yes -p ${ROOT_DIR}/env --file condalist.txt


.PHONY: test
test:
	@$(MAKE) build
	${NOSE}


