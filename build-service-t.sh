#!/bin/bash

echo "Building Service T..."
cd services/service_t

docker buildx build --no-cache --platform linux/amd64,linux/arm64 \
  -t 104013952213.dkr.ecr.eu-north-1.amazonaws.com/aharon-flask-app:map-service-t-v1 \
  --push .

echo "Service T build completed!" 