#!/bin/bash

echo "Building all microservices..."

# Build all services
./build-service-k.sh
./build-service-j.sh
./build-service-b.sh
./build-service-x.sh
./build-service-t.sh

echo "All services built successfully!"