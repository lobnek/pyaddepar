#!/usr/bin/env bash
docker-compose -f docker-compose.test.yml build --no-cache
./graph.sh
docker-compose -f docker-compose.test.yml run test-pyaddepar
docker-compose -f docker-compose.test.yml run test-pyaddepar sphinx-build /source /build

# remove all containers that are exited...
docker rm $(docker ps -q -f status=exited)

# remove the volumes hanging around...
docker volume prune -f

