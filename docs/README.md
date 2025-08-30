# UdaConnect Microservices Platform

This project is a microservices-based version of the UdaConnect platform, designed to connect people based on proximity and location events.

## 🚀 Services Overview

- **persons/**: Handles person data via REST API.
- **locations/**: Accepts location reports for persons.
- **connections/**: gRPC service to compute proximity-based connections.
- **kafka-producer/**: Publishes location events to Kafka.
- **kafka-consumer/**: Listens for location events and stores them.
- **api-gateway/**: Aggregates REST APIs and bridges REST→gRPC.

## 🐳 Local Development with Docker Compose

Start all services locally:

```bash
docker-compose up --build
```

Verify services are running:

- Persons: http://localhost:30001/persons
- Locations: http://localhost:30002/locations
- Kafka Producer: http://localhost:30003/produce/location
- API Gateway: http://localhost:30006/locations/proximity

## 🧪 Test the Platform

- Use the provided `postman.json` for REST endpoints.
- Use `grpc.txt` for testing gRPC proximity calls with curl or Python client.

## ⎈ Deploy to Kubernetes

Each microservice has a Helm chart under `kubernetes/helm/`.

Install with:

```bash
helm install persons ./kubernetes/helm/persons
```

Deploy with ArgoCD by applying the manifests in `argocd/`.

## 📂 Project Structure

```
UdaConnect/
├── modules/
│   ├── persons/
│   ├── locations/
│   ├── ...
├── docker-compose.yml
├── kubernetes/
│   └── helm/
├── argocd/
├── docs/
│   ├── grpc.txt
│   ├── postman.json
│   └── ...
└── .github/
    └── workflows/
        └── deploy.yml
```

## 📌 Technologies

- Python, Flask, SQLAlchemy
- Kafka (kafka-python)
- gRPC (grpcio)
- PostgreSQL
- Docker, Kubernetes, Helm, ArgoCD

## 👥 Authors

Yasmin Kloub