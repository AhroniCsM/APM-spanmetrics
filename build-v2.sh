#!/bin/bash

# Usage: ./build-v2.sh <service-name>
# Example: ./build-v2.sh service-k

if [ $# -eq 0 ]; then
    echo "Usage: $0 <service-name>"
    echo "Available services: service-k, service-j, service-b, service-x, service-t"
    exit 1
fi

SERVICE_NAME=$1

echo "Building $SERVICE_NAME v2..."

# Convert service-name to service_name for directory
SERVICE_DIR=$(echo $SERVICE_NAME | sed 's/-/_/g')
cd services/$SERVICE_DIR

docker buildx build --no-cache --platform linux/amd64,linux/arm64 \
  -t 104013952213.dkr.ecr.eu-north-1.amazonaws.com/aharon-flask-app:map-$SERVICE_NAME-v2 \
  --push .

echo "$SERVICE_NAME v2 build completed!" 