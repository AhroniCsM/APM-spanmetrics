#!/bin/bash

echo "Deploying Datadog microservices to Kubernetes..."

# Apply namespace first
kubectl apply -f k8s-datadog/namespace.yaml

# Apply all service deployments
kubectl apply -f k8s-datadog/service-k-deployment.yaml
kubectl apply -f k8s-datadog/service-j-deployment.yaml
kubectl apply -f k8s-datadog/service-b-deployment.yaml
kubectl apply -f k8s-datadog/service-x-deployment.yaml
kubectl apply -f k8s-datadog/service-t-deployment.yaml

echo "Datadog deployment completed!"
echo "Checking pod status..."
kubectl get pods -n map

echo "Checking services..."
kubectl get services -n map 