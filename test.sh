#!/usr/bin/env bash
docker-compose -f docker-compose.test.yml build --no-cache
docker-compose -f docker-compose.test.yml run test-pyaddepar
docker-compose -f docker-compose.test.yml run test-pyaddepar sphinx-build source build