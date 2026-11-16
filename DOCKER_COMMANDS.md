# 🦭 Podman Commands — PlantDiseaseDetector

> Complete reference of all **Podman** commands used in the **PlantDiseaseDetector** project.
> The app runs as a multi-container stack: **FastAPI (CNN API)** + **Nginx (reverse proxy)**.

> [!NOTE]
> Podman is a **daemonless, rootless**, OCI-compliant drop-in replacement for Docker.
> No root daemon required — more secure by default and native on RHEL/Fedora/OpenShift.

---

## 📁 Project Container Files

| File | Purpose |
|:--|:--|
| [`Dockerfile`](./Dockerfile) | Builds the FastAPI + TensorFlow app image |
| [`docker-compose.yml`](./docker-compose.yml) | Orchestrates FastAPI + Nginx containers |
| [`nginx/nginx.conf`](./nginx/nginx.conf) | Nginx reverse proxy configuration |
| [`.dockerignore`](./.dockerignore) | Excludes `.venv`, `.git`, and local datasets from build context |

---

## 0. ⚙️ Install Podman

```bash
# macOS (via Homebrew)
brew install podman

# Initialize and start the Podman machine (macOS only)
podman machine init
podman machine start

# Verify installation
podman --version
podman info
```

---

## 1. 🔨 Build the Image

```bash
# Build from project root (uses Dockerfile)
podman build -t plant-disease-detector:latest .

# Build with a version tag
podman build -t plant-disease-detector:v1.0.0 .

# Force fresh build — no cache
podman build --no-cache -t plant-disease-detector:latest .
```

---

## 2. ▶️ Run the Container

```bash
# Basic run — exposes API on port 8001
podman run -p 8001:8000 plant-disease-detector:latest

# Run in detached (background) mode with a name
podman run -d \
  -p 8001:8000 \
  --name plant-disease-detector-app \
  plant-disease-detector:latest

# Run with volume mounts (persist model weights + uploads)
# Note: :z flag relabels volumes for SELinux compatibility
podman run -d \
  -p 8001:8000 \
  --name plant-disease-detector-app \
  -v ./models:/app/models:ro,z \
  -v ./static/uploads:/app/static/uploads:rw,z \
  plant-disease-detector:latest
```

---

## 3. 🧩 Podman Compose (FastAPI + Nginx)

```bash
# Install podman-compose (first time only)
pip install podman-compose

# Start all services
podman-compose up

# Start in detached / background mode
podman-compose up -d

# Rebuild images before starting
podman-compose up --build

# Stop all services
podman-compose down

# Stop and remove volumes
podman-compose down -v

# View status of all services
podman-compose ps

# View live logs for all services
podman-compose logs -f

# View logs for a specific service
podman-compose logs -f plant-disease-detector
podman-compose logs -f nginx
```

> [!TIP]
> Podman 4.x+ also ships a native subcommand (no hyphen):
> ```bash
> podman compose up -d
> podman compose down
> podman compose logs -f
> ```

---

## 4. 🔍 Inspect & Manage Containers

```bash
# List running containers
podman ps

# List all containers (including stopped)
podman ps -a

# Real-time CPU / memory usage
podman stats

# View logs
podman logs plant-disease-detector-app
podman logs -f plant-disease-detector-app    # follow/live stream

# Start / stop / restart
podman start plant-disease-detector-app
podman stop plant-disease-detector-app
podman restart plant-disease-detector-app

# Remove a container
podman rm plant-disease-detector-app

# Open an interactive shell inside a running container
podman exec -it plant-disease-detector-app bash

# Check built-in health status
podman inspect --format='{{.State.Health.Status}}' plant-disease-detector-app

# View detailed container metadata
podman inspect plant-disease-detector-app
```

---

## 5. 🖼️ Image Management & Registry

```bash
# List local images
podman images

# Remove an image
podman rmi plant-disease-detector:latest

# Login to Docker Hub
podman login docker.io

# Tag image for Docker Hub (full registry path required)
podman tag plant-disease-detector:latest docker.io/gunakannan/plant-disease-detector:latest

# Push to Docker Hub
podman push docker.io/gunakannan/plant-disease-detector:latest

# Pull from Docker Hub
podman pull docker.io/gunakannan/plant-disease-detector:latest

# Push to Quay.io (Red Hat registry)
podman tag plant-disease-detector:latest quay.io/gunakannan/plant-disease-detector:latest
podman push quay.io/gunakannan/plant-disease-detector:latest
```

---

## 6. 🌐 Network & Volume

```bash
# List all Podman networks
podman network ls

# Inspect the project bridge network
podman network inspect plantdiseasedetector_plant-net

# Create a named network manually
podman network create plant-net

# List volumes
podman volume ls

# Remove a named volume
podman volume rm plant-disease-detector_uploads

# Clean up all stopped containers, unused images, and networks
podman system prune -f

# Podman system info
podman system info
```

---

## 7. ❤️ Health Check

The [`Dockerfile`](./Dockerfile) includes a built-in health check that Podman polls every **30 seconds**:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

**Verify manually:**

```bash
curl http://localhost:8001/health
# → {"status":"ok","model_loaded":true,"model_path":"models/plant_disease_model.keras"}

# Run health check via Podman
podman healthcheck run plant-disease-detector-app
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

# (macOS only) Start Podman machine
podman machine start

# Start the full stack (FastAPI + Nginx)
podman-compose up --build -d

# Check everything is healthy
podman-compose ps
curl http://localhost:8001/health

# Open the app in your browser
open http://localhost:8080

# Tear down
podman-compose down
```

---

## 10. 🔧 Generate systemd Service (Auto-start on Boot)

Podman can generate a **systemd unit file** to run the container as a service:

```bash
# Generate systemd unit file
podman generate systemd --name plant-disease-detector-app --files --new

# Install and enable the service
mv container-plant-disease-detector-app.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now container-plant-disease-detector-app.service

# Check service status
systemctl --user status container-plant-disease-detector-app.service
```

---

## 11. 🧰 Containerfile / Dockerfile Summary

```
FROM python:3.10-slim
├── Install system libs (libgl1, libglib2.0, curl)
├── WORKDIR /app
├── COPY requirements.txt → pip install
├── COPY . .
├── RUN mkdir models static/uploads + set permissions
├── USER 1001 (non-root — rootless compatible)
├── EXPOSE 8000
├── HEALTHCHECK every 30s → GET /health
└── CMD uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 12. 🐳 Docker → Podman Cheat Sheet

| Task | Old (Docker) | New (Podman) |
|:--|:--|:--|
| Build image | `docker build` | `podman build` |
| Run container | `docker run` | `podman run` |
| List containers | `docker ps` | `podman ps` |
| List images | `docker images` | `podman images` |
| View logs | `docker logs` | `podman logs` |
| Execute inside | `docker exec` | `podman exec` |
| Push image | `docker push user/img` | `podman push docker.io/user/img` |
| Pull image | `docker pull user/img` | `podman pull docker.io/user/img` |
| Compose up | `docker compose up` | `podman-compose up` |
| System cleanup | `docker system prune` | `podman system prune` |
| Run as root? | ✅ Yes (daemon) | ❌ No (rootless) |
| Requires daemon? | ✅ Yes | ❌ No |
| systemd support | ❌ Limited | ✅ Native |

> [!TIP]
> Create a shell alias so existing scripts keep working:
> ```bash
> echo "alias docker=podman" >> ~/.zshrc && source ~/.zshrc
> ```

---

*Generated for PlantDiseaseDetector · CNN-based plant leaf disease classification*
*Podman: daemonless · rootless · OCI-compliant*
