#!/usr/bin/env bash
docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml run test-pyaddepar
ret=$?

# removes also all the containers linked to this particular service "test" defined in "docker-compose.test.yml"
docker-compose -f docker-compose.test.yml rm -v -f test

exit $ret