#!/usr/bin/env bash
docker-compose -p test -f docker-compose.test.yml build
docker-compose -p test -f docker-compose.test.yml run sut
exit_code=`docker wait test_sut_run_1`
docker-compose -p test -f docker-compose.test.yml down
exit ${exit_code}
