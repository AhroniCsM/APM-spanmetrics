#!/bin/bash

echo "Building Service K..."
cd services/service_k

docker buildx build --no-cache --platform linux/amd64,linux/arm64 \
  -t 104013952213.dkr.ecr.eu-north-1.amazonaws.com/aharon-flask-app:map-service-k-v1 \
  --push .

echo "Service K build completed!" 