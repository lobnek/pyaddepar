#!/usr/bin/env bash
docker-compose -f docker-compose.test.yml build test
docker-compose -f docker-compose.test.yml run test
