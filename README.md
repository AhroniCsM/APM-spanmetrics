# Map Distribution Microservices & APM Spanmetrics

## Overview
This project demonstrates a distributed microservices architecture with integrated Application Performance Monitoring (APM) and span metrics collection. It is designed for learning, experimentation, and as a template for real-world distributed tracing and observability using OpenTelemetry and Datadog.

## Architecture

```
   service K 
           \
            service B ---- service X (main drilldown)
           /      \
   service J       \
                    service T
```

- **Service K**: Generates traffic to Service B every 3 seconds
- **Service J**: Generates traffic to Service B every 4 seconds
- **Service B**: Routes traffic from K to X, and from J to T
- **Service X**: Main service for traffic analysis and drilldown
- **Service T**: Receives traffic routed from Service J via Service B

## Features
- **Automatic Traffic Generation**: Simulates real microservice traffic
- **Conditional Routing**: Service B routes based on source
- **Comprehensive Logging**: All services log requests and internal logic
- **Health Checks**: `/health` endpoint for all services
- **Traffic Analysis**: Service X exposes `/traffic` endpoint
- **OpenTelemetry Ready**: All deployments include OTEL annotations
- **Datadog Integration**: Optional Datadog tracing manifests

## Quick Start

### Prerequisites
- Docker (with buildx support)
- Kubernetes cluster (minikube, kind, or cloud)
- `kubectl` configured
- AWS ECR access (for pulling images)

### Build All Services
```bash
chmod +x *.sh
./build-all.sh
```

### Deploy to Kubernetes
```bash
./deploy.sh
```

### Verify Deployment
```bash
kubectl get pods -n map
kubectl get services -n map
```

### Deploy with Datadog (Optional)
```bash
./deploy-datadog.sh
```

## Service Endpoints
- `GET /` - Service info and status
- `GET /health` - Health check
- **Service X**: `GET /traffic` - Traffic analysis
- **Service T**: `GET /traffic` - Traffic data

## File Structure
```
.
├── services/                  # Source code for each microservice
│   ├── service-k/
│   ├── service-j/
│   ├── service-b/
│   ├── service-x/
│   └── service-t/
├── k8s/                       # Kubernetes manifests (OpenTelemetry)
│   ├── namespace.yaml
│   ├── service-*-deployment.yaml
├── k8s-datadog/               # Kubernetes manifests (Datadog)
├── build-*.sh                 # Build scripts
├── deploy*.sh                 # Deployment scripts
├── otel-override.yaml         # OpenTelemetry Collector config
└── README.md
```

## Monitoring & Debugging
- View logs: `kubectl logs -n map deployment/service-x`
- Port forward: `kubectl port-forward -n map service/service-x 8080:5003`
- Visit: [http://localhost:8080/traffic](http://localhost:8080/traffic)

## Development
- Run any service locally:
  ```bash
  cd services/service-k
  pip install -r requirements.txt
  python app.py
  ```
- Environment variables:
  - `SERVICE_PORT` - Port to run the service
  - `SERVICE_B_URL` - URL for Service B (used by K and J)
  - `SERVICE_X_URL` - URL for Service X (used by B)
  - `SERVICE_T_URL` - URL for Service T (used by B)

## Troubleshooting
- **Image Pull Errors**: Check AWS ECR credentials
- **Pod Not Ready**: Check logs and events (`kubectl get events -n map`)
- **Port Conflicts**: Ensure unique ports per service

## Contributing
Pull requests and issues are welcome! Please open an issue to discuss major changes first.

## License
MIT 