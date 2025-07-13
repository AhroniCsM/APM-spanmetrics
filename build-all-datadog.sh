#!/bin/bash

echo "Building all Datadog microservices..."

# Build all services
./build-datadog-service-k.sh
./build-datadog-service-j.sh
./build-datadog-service-b.sh
./build-datadog-service-x.sh
./build-datadog-service-t.sh

echo "All Datadog services built successfully!" 