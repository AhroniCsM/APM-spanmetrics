#!/bin/bash

echo "Building Service J (Datadog)..."
cd services-datadog/service_j

docker buildx build --no-cache --platform linux/amd64,linux/arm64 \
  -t 104013952213.dkr.ecr.eu-north-1.amazonaws.com/aharon-flask-app:map-service-datadog-j-v4 \
  --push .

echo "Service J (Datadog) build completed!"