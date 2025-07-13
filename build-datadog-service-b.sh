#!/bin/bash

echo "Building Service B (Datadog)..."
cd services-datadog/service_b

docker buildx build --no-cache --platform linux/amd64,linux/arm64 \
  -t 104013952213.dkr.ecr.eu-north-1.amazonaws.com/aharon-flask-app:map-service-datadog-b-v4 \
  --push .

echo "Service B (Datadog) build completed!" 