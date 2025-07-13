#!/bin/bash

echo "Testing services locally..."

# Function to start a service in background
start_service() {
    local service_name=$1
    local port=$2
    local service_dir="services/$service_name"
    
    echo "Starting $service_name on port $port..."
    cd $service_dir
    python app.py &
    cd ../..
    sleep 2
}

# Function to test service health
test_health() {
    local service_name=$1
    local port=$2
    
    echo "Testing $service_name health..."
    curl -s http://localhost:$port/health | jq . || echo "Failed to get health from $service_name"
}

# Start services in order (dependencies first)
start_service "service-x" 5003
start_service "service-t" 5004
start_service "service-b" 5001
start_service "service-k" 5000
start_service "service-j" 5002

echo "All services started. Testing health endpoints..."

# Test health endpoints
test_health "service-x" 5003
test_health "service-t" 5004
test_health "service-b" 5001
test_health "service-k" 5000
test_health "service-j" 5002

echo "Waiting 10 seconds for traffic to flow..."
sleep 10

echo "Checking traffic in Service X..."
curl -s http://localhost:5003/traffic | jq .

echo "Checking traffic in Service T..."
curl -s http://localhost:5004/traffic | jq .

echo "Test completed. Press Ctrl+C to stop all services."
echo "Services are running on:"
echo "  Service K: http://localhost:5000"
echo "  Service J: http://localhost:5002"
echo "  Service B: http://localhost:5001"
echo "  Service X: http://localhost:5003"
echo "  Service T: http://localhost:5004"

# Wait for user to stop
wait 