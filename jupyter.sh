#!/usr/bin/env bash
echo "http://localhost:8883"
docker-compose run -p "8883:8888" jupyter
