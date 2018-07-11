#!/usr/bin/env bash
docker build --file Dockerfile --target test --tag pyaddepar:test .

# delete all files in html-coverage
rm -rf $(pwd)/html-coverage/*

# run all tests, seems to be slow on teamcity
docker run --rm -v $(pwd)/html-coverage/:/html-coverage -v $(pwd)/html-report:/html-report pyaddepar:test

ret=$?

docker run --rm -v $(pwd)/source:/pyaddepar/source:ro -v $(pwd)/build:/pyaddepar/build pyaddepar:test sphinx-build source build

docker rmi pyaddepar:test

exit $ret
