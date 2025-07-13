#!/bin/bash

echo "Deploying microservices to Kubernetes..."

# Apply namespace first
kubectl apply -f k8s/namespace.yaml

# Apply all service deployments
kubectl apply -f k8s/service-k-deployment.yaml
kubectl apply -f k8s/service-j-deployment.yaml
kubectl apply -f k8s/service-b-deployment.yaml
kubectl apply -f k8s/service-x-deployment.yaml
kubectl apply -f k8s/service-t-deployment.yaml

echo "Deployment completed!"
echo "Checking pod status..."
kubectl get pods -n map

echo "Checking services..."
kubectl get services -n map 