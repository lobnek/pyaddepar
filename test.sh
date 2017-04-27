#!/usr/bin/env bash
docker build --file Dockerfile-Test --tag pyaddepar:latest .

# run all tests, seems to be slow on teamcity
docker run --rm pyaddepar:latest

ret=$?

exit $ret
