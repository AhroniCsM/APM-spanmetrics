#!/bin/bash

echo "Building Service K (Datadog)..."
cd services-datadog/service_k

docker buildx build --no-cache --platform linux/amd64,linux/arm64 \
  -t 104013952213.dkr.ecr.eu-north-1.amazonaws.com/aharon-flask-app:map-service-datadog-k-v4 \
  --push .

echo "Service K (Datadog) build completed!" 