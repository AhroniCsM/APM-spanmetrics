#!/bin/bash

echo "Building Service X..."
cd services/service_x

docker buildx build --no-cache --platform linux/amd64,linux/arm64 \
  -t 104013952213.dkr.ecr.eu-north-1.amazonaws.com/aharon-flask-app:map-service-x-v1 \
  --push .

echo "Service X build completed!" 