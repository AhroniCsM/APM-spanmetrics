#!/bin/bash

echo "Building Service J..."
cd services/service_j

docker buildx build --no-cache --platform linux/amd64,linux/arm64 \
  -t 104013952213.dkr.ecr.eu-north-1.amazonaws.com/aharon-flask-app:map-service-j-v1 \
  --push .

echo "Service J build completed!" 