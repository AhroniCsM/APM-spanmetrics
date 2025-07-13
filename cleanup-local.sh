#!/bin/bash

echo "Stopping all local services..."

# Kill all Python processes running on our service ports
pkill -f "python.*app.py" || true

# Kill any processes on our service ports
for port in 5000 5001 5002 5003 5004; do
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
done

echo "All services stopped." 