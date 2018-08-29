#!/usr/bin/env bash
docker-compose -f docker-compose.test.yml run test sphinx-build /source artifacts/build