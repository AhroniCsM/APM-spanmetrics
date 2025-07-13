#!/bin/bash

echo "Verifying Kubernetes deployment..."

# Check namespace
echo "=== Checking namespace ==="
kubectl get namespace map

# Check pods
echo -e "\n=== Checking pod status ==="
kubectl get pods -n map -o wide

# Check services
echo -e "\n=== Checking services ==="
kubectl get services -n map

# Check endpoints
echo -e "\n=== Checking endpoints ==="
kubectl get endpoints -n map

# Check recent events
echo -e "\n=== Recent events ==="
kubectl get events -n map --sort-by='.lastTimestamp' | tail -10

# Wait for pods to be ready
echo -e "\n=== Waiting for pods to be ready ==="
kubectl wait --for=condition=ready pod -l app=service-k -n map --timeout=300s
kubectl wait --for=condition=ready pod -l app=service-j -n map --timeout=300s
kubectl wait --for=condition=ready pod -l app=service-b -n map --timeout=300s
kubectl wait --for=condition=ready pod -l app=service-x -n map --timeout=300s
kubectl wait --for=condition=ready pod -l app=service-t -n map --timeout=300s

echo -e "\n=== All pods are ready! ==="

# Check logs for traffic flow
echo -e "\n=== Checking Service X logs for traffic ==="
kubectl logs -n map deployment/service-x --tail=10

echo -e "\n=== Checking Service T logs for traffic ==="
kubectl logs -n map deployment/service-t --tail=10

echo -e "\n=== Deployment verification completed! ==="
echo "To monitor traffic flow, run:"
echo "kubectl port-forward -n map service/service-x 8080:5003"
echo "Then visit http://localhost:8080/traffic" 