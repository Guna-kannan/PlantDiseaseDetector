# 🐳 Docker Commands — PlantDiseaseDetector

> Complete reference of all Docker commands used in the **PlantDiseaseDetector** project.
> The app runs as a multi-container stack: **FastAPI (CNN API)** + **Nginx (reverse proxy)**.

---

## 📁 Project Docker Files

| File | Purpose |
|:--|:--|
| [`Dockerfile`](./Dockerfile) | Builds the FastAPI + TensorFlow app image |
| [`docker-compose.yml`](./docker-compose.yml) | Orchestrates FastAPI + Nginx containers |
| [`nginx/nginx.conf`](./nginx/nginx.conf) | Nginx reverse proxy configuration |
| [`.dockerignore`](./.dockerignore) | Excludes `.venv`, `.git`, and local datasets from build context |

---

## 1. 🔨 Build the Image

```bash
# Build from project root (uses Dockerfile)
docker build -t plant-disease-detector:latest .

# Build with a version tag
docker build -t plant-disease-detector:v1.0.0 .

# Force fresh build — no cache
docker build --no-cache -t plant-disease-detector:latest .
```

---

## 2. ▶️ Run the Container

```bash
# Basic run — exposes API on port 8001
docker run -p 8001:8000 plant-disease-detector:latest

# Run in detached (background) mode with a name
docker run -d \
  -p 8001:8000 \
  --name plant-disease-detector-app \
  plant-disease-detector:latest

# Run with volume mounts (persist model weights + uploads)
docker run -d \
  -p 8001:8000 \
  --name plant-disease-detector-app \
  -v ./models:/app/models:ro \
  -v ./static/uploads:/app/static/uploads:rw \
  plant-disease-detector:latest
```

---

## 3. 🧩 Docker Compose (FastAPI + Nginx)

```bash
# Start all services
docker compose up

# Start in detached / background mode
docker compose up -d

# Rebuild images before starting
docker compose up --build

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# View status of all services
docker compose ps

# View live logs for all services
docker compose logs -f

# View logs for a specific service
docker compose logs -f plant-disease-detector
docker compose logs -f nginx
```

---

## 4. 🔍 Inspect & Manage Containers

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Real-time CPU / memory usage
docker stats

# View logs
docker logs plant-disease-detector-app
docker logs -f plant-disease-detector-app    # follow/live stream

# Start / stop / restart
docker start plant-disease-detector-app
docker stop plant-disease-detector-app
docker restart plant-disease-detector-app

# Remove a container
docker rm plant-disease-detector-app

# Open an interactive shell inside a running container
docker exec -it plant-disease-detector-app bash

# Check built-in health status
docker inspect --format='{{.State.Health.Status}}' plant-disease-detector-app
```

---

## 5. 🖼️ Image Management & Registry

```bash
# List local images
docker images

# Remove an image
docker rmi plant-disease-detector:latest

# Tag image for Docker Hub
docker tag plant-disease-detector:latest gunakannan/plant-disease-detector:latest

# Push to Docker Hub
docker push gunakannan/plant-disease-detector:latest

# Pull from Docker Hub
docker pull gunakannan/plant-disease-detector:latest
```

---

## 6. 🌐 Network & Volume

```bash
# List all Docker networks
docker network ls

# Inspect the project bridge network
docker network inspect plantdiseasedetector_plant-net

# List Docker volumes
docker volume ls

# Clean up all stopped containers, unused images, and networks
docker system prune -f
```

---

## 7. ❤️ Health Check

The [`Dockerfile`](./Dockerfile) includes a built-in health check that Docker polls every **30 seconds**:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

**Verify manually:**

```bash
curl http://localhost:8001/health
# → {"status":"ok","model_loaded":true,"model_path":"models/plant_disease_model.keras"}
```

---

## 8. 🗺️ Port Mapping Reference

| Service | Container Port | Host Port | URL |
|:--|:--:|:--:|:--|
| FastAPI (direct access) | `8000` | `8001` | http://localhost:8001 |
| Nginx (reverse proxy) | `80` | `8080` | http://localhost:8080 |
| Health Check endpoint | `8000` | `8001` | http://localhost:8001/health |
| Prediction API | `8000` | `8001` | http://localhost:8001/predict |

---

## 9. ⚡ Quick Start (Full Stack)

```bash
# Clone the repo
git clone https://github.com/Guna-kannan/PlantDiseaseDetector.git
cd PlantDiseaseDetector

# Start the full stack (FastAPI + Nginx)
docker compose up --build -d

# Check everything is healthy
docker compose ps
curl http://localhost:8001/health

# Open the app in your browser
open http://localhost:8080

# Tear down
docker compose down
```

---

## 10. 🧰 Dockerfile Summary

```
FROM python:3.10-slim
├── Install system libs (libgl1, libglib2.0, curl)
├── WORKDIR /app
├── COPY requirements.txt → pip install
├── COPY . .
├── RUN mkdir models static/uploads + set permissions
├── USER 1001 (non-root)
├── EXPOSE 8000
├── HEALTHCHECK every 30s → GET /health
└── CMD uvicorn app:app --host 0.0.0.0 --port 8000
```

---

*Generated for PlantDiseaseDetector · CNN-based plant leaf disease classification*
