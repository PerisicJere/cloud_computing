#!/bin/bash
docker build -t rest-api .

docker stop api-server 2>/dev/null || true
docker rm api-server 2>/dev/null || true

echo "Starting API.."
docker run -p 9999:9999 --name api-server rest-api

docker ps | grep api-server

echo "http://localhost:9999"
