#!/usr/bin/env bash
docker-compose -f docker-compose.test.yml build
./graph.sh

docker-compose -f docker-compose.test.yml run test-pyaddepar
ret=$?

docker-compose -f docker-compose.test.yml run test-pyaddepar sphinx-build /source artifacts/build

# removes also all the containers linked to this particular service "test" defined in "docker-compose.test.yml"
docker-compose -f docker-compose.test.yml rm -v -f test

exit $ret