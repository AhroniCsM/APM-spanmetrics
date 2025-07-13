#!/bin/bash

echo "Building Service B..."
cd services/service_b

docker buildx build --no-cache --platform linux/amd64,linux/arm64 \
  -t 104013952213.dkr.ecr.eu-north-1.amazonaws.com/aharon-flask-app:map-service-b-v1 \
  --push .

echo "Service B build completed!" 