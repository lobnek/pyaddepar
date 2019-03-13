#!/usr/bin/env bash
source .env
echo "http://localhost:${PORT}"
docker-compose up jupyter
