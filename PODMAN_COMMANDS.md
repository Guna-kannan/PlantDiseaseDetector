# 🦭 Podman Commands — PlantDiseaseDetector

> Complete reference of all **Podman** commands used in the **PlantDiseaseDetector** project.
> Podman is a **daemonless, rootless** drop-in replacement for Docker — most `docker` commands work identically by replacing `docker` with `podman`.

> [!NOTE]
> **Why Podman over Docker?**
> - Runs **without a root daemon** (more secure by default)
> - Each container runs as a **non-root user** (rootless mode)
> - Compatible with **OCI** (Open Container Initiative) standards
> - Native **systemd** integration (`podman generate systemd`)
> - Preferred on **RHEL / Fedora / OpenShift** environments

---

## 📁 Project Container Files

| File | Purpose |
|:--|:--|
| [`Dockerfile`](./Dockerfile) | Builds the FastAPI + TensorFlow app image (OCI-compatible) |
| [`docker-compose.yml`](./docker-compose.yml) | Orchestrates FastAPI + Nginx containers |
| [`nginx/nginx.conf`](./nginx/nginx.conf) | Nginx reverse proxy configuration |
| [`.dockerignore`](./.dockerignore) | Excludes `.venv`, `.git`, and local datasets from build context |

> [!TIP]
> Podman reads the same `Dockerfile` and `.dockerignore` as Docker — no changes needed to these files.

---

## 0. ⚙️ Install Podman (if not already installed)

```bash
# macOS (via Homebrew)
brew install podman

# Initialize and start the Podman machine (macOS only — creates a Linux VM)
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
podman run -d \
  -p 8001:8000 \
  --name plant-disease-detector-app \
  -v ./models:/app/models:ro,z \
  -v ./static/uploads:/app/static/uploads:rw,z \
  plant-disease-detector:latest
```

> [!IMPORTANT]
> The `:z` flag on volume mounts is **Podman-specific** — it relabels the volume for SELinux compatibility (required on RHEL/Fedora). Use `:Z` for a private, unshared label.

---

## 3. 🧩 Podman Compose (FastAPI + Nginx)

```bash
# Install podman-compose (if not already installed)
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

> [!NOTE]
> **Podman 4.x+** also ships a native `podman compose` subcommand (no hyphen) that can call `docker-compose` or `podman-compose` as the backend:
> ```bash
> podman compose up -d
> podman compose down
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

# Tag image for Docker Hub (Podman requires full registry path)
podman tag plant-disease-detector:latest docker.io/gunakannan/plant-disease-detector:latest

# Login to Docker Hub
podman login docker.io

# Push to Docker Hub
podman push docker.io/gunakannan/plant-disease-detector:latest

# Pull from Docker Hub
podman pull docker.io/gunakannan/plant-disease-detector:latest

# Push to Quay.io (Red Hat registry — preferred with Podman)
podman tag plant-disease-detector:latest quay.io/gunakannan/plant-disease-detector:latest
podman push quay.io/gunakannan/plant-disease-detector:latest
```

> [!NOTE]
> Unlike Docker, Podman requires the **full registry path** (e.g., `docker.io/`) when pushing or pulling. No implicit `docker.io` prefix is assumed.

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

# Check Podman system info
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

# Check container health via Podman
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

## 9. ⚡ Quick Start (Full Stack with Podman)

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

## 10. 🔧 Generate systemd Service (Podman-only feature)

Podman can auto-generate a **systemd unit file** to run the container as a system service (auto-start on boot):

```bash
# Generate systemd unit file for the container
podman generate systemd --name plant-disease-detector-app --files --new

# Install and enable the service (run on boot)
mv container-plant-disease-detector-app.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now container-plant-disease-detector-app.service

# Check service status
systemctl --user status container-plant-disease-detector-app.service
```

---

## 11. 🐳 Docker vs Podman Cheat Sheet

| Command | Docker | Podman |
|:--|:--|:--|
| Build image | `docker build` | `podman build` |
| Run container | `docker run` | `podman run` |
| List containers | `docker ps` | `podman ps` |
| List images | `docker images` | `podman images` |
| View logs | `docker logs` | `podman logs` |
| Execute inside | `docker exec` | `podman exec` |
| Push image | `docker push` | `podman push docker.io/...` |
| Pull image | `docker pull` | `podman pull docker.io/...` |
| Compose up | `docker compose up` | `podman-compose up` |
| System cleanup | `docker system prune` | `podman system prune` |
| Run as root? | ✅ Yes (daemon) | ❌ No (rootless by default) |
| Requires daemon? | ✅ Yes | ❌ No |
| systemd support | ❌ Limited | ✅ Native |

> [!TIP]
> You can also create a shell alias to use `docker` as a shortcut for `podman`:
> ```bash
> echo "alias docker=podman" >> ~/.zshrc && source ~/.zshrc
> ```

---

## 12. 🧰 Dockerfile Summary

```
FROM python:3.10-slim
├── Install system libs (libgl1, libglib2.0, curl)
├── WORKDIR /app
├── COPY requirements.txt → pip install
├── COPY . .
├── RUN mkdir models static/uploads + set permissions
├── USER 1001 (non-root — Podman rootless compatible)
├── EXPOSE 8000
├── HEALTHCHECK every 30s → GET /health
└── CMD uvicorn app:app --host 0.0.0.0 --port 8000
```

> [!NOTE]
> The `USER 1001` in the Dockerfile already makes the image **rootless-friendly**, which aligns perfectly with Podman's security model.

---

*Generated for PlantDiseaseDetector · CNN-based plant leaf disease classification*
*Podman: daemonless, rootless, OCI-compliant container engine*
