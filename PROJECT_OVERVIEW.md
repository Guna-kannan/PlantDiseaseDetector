# 🌿 PlantDiseaseDetector — Complete Project Overview

> **CNN-based plant leaf disease classification** with a FastAPI web application, containerized using Podman/Docker, orchestrated with Compose, Kubernetes, and OpenShift.

---

## 📋 Table of Contents

1. [About the Project](#1-about-the-project)
2. [Supported Disease Classes](#2-supported-disease-classes)
3. [Tech Stack](#3-tech-stack)
4. [Project Structure](#4-project-structure)
5. [CNN Model Details](#5-cnn-model-details)
6. [REST API Reference](#6-rest-api-reference)
7. [Local Development Setup](#7-local-development-setup)
8. [Podman Commands](#8-podman-commands)
9. [Docker Compose Commands](#9-docker-compose-commands)
10. [Kubernetes Commands](#10-kubernetes-commands)
11. [OpenShift Commands](#11-openshift-commands)
12. [Linux Administration Commands (Unit 1)](#12-linux-administration-commands-unit-1)
13. [Port Mapping Reference](#13-port-mapping-reference)
14. [Git Commands](#14-git-commands)

---

## 1. About the Project

**PlantDiseaseDetector** is an end-to-end machine learning web application that classifies plant leaf diseases from uploaded images using a **Convolutional Neural Network (CNN)** trained on the **PlantVillage** dataset.

**What it does:**
- Upload a leaf photo → get instant disease diagnosis
- Returns: disease class, confidence %, severity level, treatment recommendation, top-3 candidates
- Supports **15 disease classes** across Tomato, Potato, and Bell Pepper crops
- Served via a **FastAPI** backend with an **Nginx** reverse proxy

**Who made it:**
| Name | Roll Number |
|:--|:--|
| Satya Sriram Prakash P | RA2411026010501 |
| Guna K | RA2411026010476 |
| Shahma Saidali Thoppasheri | RA2411026010434 |

**Guide:** Dr. Prabakaran J, Assistant Professor, Department of Networking and Communications

---

## 2. Supported Disease Classes

| # | Class | Crop | Severity |
|:--|:--|:--|:--|
| 1 | `Pepper__bell___Bacterial_spot` | Bell Pepper | 🟡 Moderate |
| 2 | `Pepper__bell___healthy` | Bell Pepper | 🟢 None |
| 3 | `Potato___Early_blight` | Potato | 🟡 Moderate |
| 4 | `Potato___Late_blight` | Potato | 🔴 High |
| 5 | `Potato___healthy` | Potato | 🟢 None |
| 6 | `Tomato_Bacterial_spot` | Tomato | 🟡 Moderate |
| 7 | `Tomato_Early_blight` | Tomato | 🟡 Moderate |
| 8 | `Tomato_Late_blight` | Tomato | 🔴 High |
| 9 | `Tomato_Leaf_Mold` | Tomato | 🟡 Moderate |
| 10 | `Tomato_Septoria_leaf_spot` | Tomato | 🟡 Moderate |
| 11 | `Tomato_Spider_mites_Two_spotted_spider_mite` | Tomato | 🟡 Moderate |
| 12 | `Tomato__Target_Spot` | Tomato | 🟡 Moderate |
| 13 | `Tomato__Tomato_YellowLeaf__Curl_Virus` | Tomato | 🔴 High |
| 14 | `Tomato__Tomato_mosaic_virus` | Tomato | 🔴 High |
| 15 | `Tomato_healthy` | Tomato | 🟢 None |

---

## 3. Tech Stack

| Layer | Technology |
|:--|:--|
| **ML Framework** | TensorFlow / Keras 2.15, NumPy, Pillow |
| **Web Backend** | FastAPI, Uvicorn, Jinja2 |
| **Frontend** | HTML5, CSS3, Vanilla JS (dark-themed UI) |
| **Container Engine** | Podman 5.x (rootless, daemonless) + Docker |
| **Reverse Proxy** | Nginx (Alpine) |
| **Compose** | Podman Compose / Docker Compose |
| **Orchestration** | Kubernetes (kubectl + kustomize) |
| **Cloud Platform** | Red Hat OpenShift (oc CLI) |
| **Registry** | Quay.io / Docker Hub |
| **Language** | Python 3.10 |
| **OS** | RHEL / Debian / macOS (Apple M4) |

---

## 4. Project Structure

```
PlantDiseaseDetector/
│
├── app.py                        ← FastAPI application (routes, startup, error handlers)
├── requirements.txt              ← Python dependencies
├── Containerfile                 ← OCI/Podman-compliant container spec (RHEL-ready)
├── Dockerfile                    ← Docker-compatible container spec
├── docker-compose.yml            ← Multi-container: FastAPI + Nginx + plant-net bridge
│
├── src/
│   ├── model.py                  ← CNN architecture, dataset loading, training, evaluation
│   └── predictor.py              ← Inference pipeline + disease metadata enrichment
│
├── templates/
│   └── index.html                ← Web UI (upload form, result display, top-3 chart)
│
├── static/uploads/               ← Uploaded images for inference
│
├── models/
│   ├── plant_disease_model.keras ← Trained CNN weights
│   ├── training_history.png      ← Loss/accuracy training curves
│   └── confusion_matrix.png      ← 15-class confusion matrix
│
├── nginx/
│   └── nginx.conf                ← Reverse proxy config (gzip, proxy headers)
│
├── k8s/                          ← Kubernetes manifests
│   ├── namespace.yaml
│   ├── pvc.yaml
│   ├── deployment.yaml           ← 2 replicas, liveness/readiness probes
│   ├── service.yaml
│   ├── ingress.yaml
│   └── kustomization.yaml        ← Single-command deploy bundle
│
├── openshift/                    ← OpenShift manifests
│   ├── imagestream.yaml
│   ├── buildconfig.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── route.yaml                ← Edge-terminated HTTPS Route
│
├── scripts/                      ← Automated unit demo scripts
│   ├── unit1_linux_basics.sh
│   ├── unit2_podman_workflow.sh
│   ├── unit3_registry_workflow.sh
│   ├── unit4_compose_ops.sh
│   └── unit5_k8s_openshift.sh
│
├── screenshots/                  ← Evidence screenshots for submission
├── README.md
├── PROJECT_OVERVIEW.md           ← This file
├── DOCKER_COMMANDS.md            ← All Podman commands reference
└── PODMAN_COMMANDS.md            ← Extended Podman guide
```

---

## 5. CNN Model Details

| Parameter | Value |
|:--|:--|
| **Architecture** | 6-Block CNN → Flatten → Dense(256) → Dropout(0.35) → Softmax(15) |
| **Input Shape** | 224 × 224 × 3 (RGB) |
| **Normalization** | Internal `Rescaling(1/255)` layer (no double-normalization) |
| **Augmentation** | RandomFlip, RandomRotation(0.15), RandomZoom(0.1), RandomTranslation |
| **Dataset** | PlantVillage — 20,638 images across 15 classes |
| **Split** | 80% Train / 10% Validation / 10% Test (seed=123, deterministic) |
| **Optimizer** | Adam (lr=1e-3), ReduceLROnPlateau (factor=0.4, patience=2) |
| **Early Stopping** | patience=3, restore best weights |
| **Model File** | `models/plant_disease_model.keras` (11.7 MB) |
| **Training Curves** | `models/training_history.png` |
| **Confusion Matrix** | `models/confusion_matrix.png` |

**Train the model:**
```bash
python -m src.model data/PlantVillage
```

---

## 6. REST API Reference

| Endpoint | Method | Description | Response |
|:--|:--|:--|:--|
| `/` | GET | Web UI (upload form) | HTML |
| `/predict` | POST | Upload image → get diagnosis | JSON |
| `/health` | GET | App & model health check | JSON |
| `/classes` | GET | List all 15 disease classes | JSON |
| `/docs` | GET | Swagger interactive API docs | HTML |

**Predict — Sample Request:**
```bash
curl -X POST -F "file=@leaf.jpg" http://localhost:8001/predict
```

**Predict — Sample Response:**
```json
{
  "predicted_class": "Potato___Early_blight",
  "confidence": 95.29,
  "description": "Early blight forms dark concentric rings on older leaves.",
  "treatment": "Remove affected foliage, rotate crops, apply fungicide.",
  "severity": "Moderate",
  "is_healthy": false,
  "top3": [
    {"class": "Potato___Early_blight", "confidence": 95.29},
    {"class": "Tomato_Septoria_leaf_spot", "confidence": 4.27},
    {"class": "Tomato_Bacterial_spot", "confidence": 0.26}
  ]
}
```

**Health Check:**
```bash
curl http://localhost:8001/health
# → {"status":"ok","model_loaded":true,"model_path":"models/plant_disease_model.keras"}
```

---

## 7. Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/Guna-kannan/PlantDiseaseDetector.git
cd PlantDiseaseDetector

# 2. Create Python virtual environment
python3.10 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Train model (skip if model already exists)
python -m src.model data/PlantVillage

# 5. Start the development server
uvicorn app:app --host 0.0.0.0 --port 8001 --reload

# Open in browser
open http://localhost:8001
```

---

## 8. Podman Commands

### Setup
```bash
# Install (macOS)
brew install podman

# Initialize and start Podman machine (macOS only)
podman machine init
podman machine start

# Check version and info
podman --version
podman info
```

### Build
```bash
# Build image using Containerfile (OCI/Podman standard)
podman build -f Containerfile -t plant-disease-detector:latest .

# Build with version tag
podman build -t plant-disease-detector:v1.0.0 .

# Build without cache
podman build --no-cache -t plant-disease-detector:latest .
```

### Run
```bash
# Basic run
podman run -p 8001:8000 plant-disease-detector:latest

# Detached mode with name
podman run -d \
  -p 8001:8000 \
  --name plant-disease-detector-app \
  plant-disease-detector:latest

# With volume mounts + SELinux labels (:z)
podman run -d \
  -p 8001:8000 \
  --name plant-disease-detector-app \
  -v ./models:/app/models:ro,z \
  -v ./static/uploads:/app/static/uploads:rw,z \
  plant-disease-detector:latest
```

### Manage Containers
```bash
podman ps                          # List running containers
podman ps -a                       # List all containers
podman stats                       # CPU/memory usage
podman logs -f plant-disease-detector-app   # Follow logs
podman start plant-disease-detector-app
podman stop plant-disease-detector-app
podman restart plant-disease-detector-app
podman rm plant-disease-detector-app
podman exec -it plant-disease-detector-app bash
podman inspect plant-disease-detector-app
podman healthcheck run plant-disease-detector-app
```

### Images & Registry
```bash
podman images                                       # List images
podman rmi plant-disease-detector:latest            # Remove image
podman history plant-disease-detector:latest        # Layer history

podman login docker.io
podman tag plant-disease-detector:latest docker.io/gunakannan/plant-disease-detector:latest
podman push docker.io/gunakannan/plant-disease-detector:latest
podman pull docker.io/gunakannan/plant-disease-detector:latest

# Quay.io (Red Hat registry)
podman login quay.io
podman tag plant-disease-detector:latest quay.io/gunakannan/plant-disease-detector:latest
podman push quay.io/gunakannan/plant-disease-detector:latest
```

### Pod Management (Podman-native)
```bash
# Create a shared-network pod
podman pod create --name plant-pod -p 8001:8000

# Run container inside the pod
podman run -d --pod plant-pod --name plant-detector-app plant-disease-detector:latest

podman pod ps                      # List pods
podman pod stop plant-pod
podman pod rm -f plant-pod
```

### Network & Volume
```bash
podman network ls
podman network inspect plantdiseasedetector_plant-net
podman network create plant-net
podman volume ls
podman system prune -f             # Cleanup unused resources
```

### systemd Auto-start (Podman-only)
```bash
podman generate systemd --name plant-disease-detector-app --files --new
mv container-plant-disease-detector-app.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now container-plant-disease-detector-app.service
systemctl --user status container-plant-disease-detector-app.service
```

---

## 9. Docker Compose Commands

The `docker-compose.yml` runs **FastAPI** (port 8001) + **Nginx** (port 8080) on a shared `plant-net` bridge network.

```bash
# Build and start all services
podman-compose up --build -d
# or
docker compose up --build -d

# View running services
podman-compose ps

# Follow live logs
podman-compose logs -f

# Logs for a specific service
podman-compose logs -f plant-disease-detector
podman-compose logs -f nginx

# Stop services (keep containers)
podman-compose stop

# Restart stopped services
podman-compose start

# Teardown completely
podman-compose down

# Teardown + remove volumes
podman-compose down -v
```

**Services defined in `docker-compose.yml`:**

| Service | Image | Port | Role |
|:--|:--|:--|:--|
| `plant-disease-detector` | Built from `Dockerfile` | `8001:8000` | FastAPI ML API |
| `nginx` | `nginx:alpine` | `8080:80` | Reverse proxy |

---

## 10. Kubernetes Commands

```bash
# Deploy all resources (Namespace, PVC, Deployment, Service, Ingress)
kubectl apply -k k8s/

# Check pods (2 replicas)
kubectl get pods -n plant-disease-detector -o wide

# Check all resources
kubectl get all -n plant-disease-detector
kubectl get svc,pvc,ingress -n plant-disease-detector

# Check rollout status
kubectl rollout status deployment/plant-disease-detector -n plant-disease-detector

# View logs (all pods)
kubectl logs -l app=plant-disease-detector -n plant-disease-detector --all-containers=true -f

# Shell into pod
kubectl exec -it <pod-name> -n plant-disease-detector -- /bin/sh

# Describe pod (troubleshoot ImagePullBackOff, CrashLoopBackOff)
kubectl describe pod <pod-name> -n plant-disease-detector

# View events
kubectl get events -n plant-disease-detector --sort-by='.metadata.creationTimestamp'

# Delete all resources
kubectl delete -k k8s/
```

**K8s Manifest Files:**

| File | Purpose |
|:--|:--|
| `k8s/namespace.yaml` | Dedicated namespace `plant-disease-detector` |
| `k8s/pvc.yaml` | PersistentVolumeClaim for model weights |
| `k8s/deployment.yaml` | 2-replica deployment with liveness/readiness probes |
| `k8s/service.yaml` | ClusterIP service |
| `k8s/ingress.yaml` | Ingress routing |
| `k8s/kustomization.yaml` | Single-command bundle (`kubectl apply -k k8s/`) |

---

## 11. OpenShift Commands

```bash
# Login
oc login -u <username> -p <password> https://api.crc.testing:6443

# Create project
oc new-project plant-disease-detector

# Apply manifests
oc apply -f openshift/imagestream.yaml
oc apply -f openshift/buildconfig.yaml

# Trigger in-cluster build from Git
oc start-build plant-disease-detector --follow

# Deploy app
oc apply -f openshift/deployment.yaml
oc apply -f openshift/service.yaml
oc apply -f openshift/route.yaml

# Get public Route URL
oc get route plant-disease-detector -o jsonpath='{.spec.host}'

# Check status
oc get pods
oc get route
oc logs -f <pod-name>
```

---

## 12. Linux Administration Commands (Unit 1)

```bash
# System info
uname -a
cat /etc/os-release

# File searching
grep -rn "CLASS_NAMES" src/
grep -rn "predict" app.py

# Archiving
tar -cvf backup.tar models/
gzip -k backup.tar            # → backup.tar.gz
bzip2 -k backup.tar           # → backup.tar.bz2
tar -xvf backup.tar           # Extract

# File permissions
ls -l models/
chmod 644 models/plant_disease_model.keras      # rw-r--r--
chmod -R g+rwX /app                             # group read-write-execute
chown -R 1001:0 /app                            # Set owner for containers

# Disk usage
df -h .
du -sh models/

# User management
id
groups
sudo useradd -m -s /bin/bash appuser
sudo groupadd appgroup
sudo usermod -aG appgroup appuser

# Run all Unit 1 demos
./scripts/unit1_linux_basics.sh
./scripts/unit2_podman_workflow.sh
./scripts/unit3_registry_workflow.sh
./scripts/unit4_compose_ops.sh
./scripts/unit5_k8s_openshift.sh
```

---

## 13. Port Mapping Reference

| Service | Container Port | Host Port | URL |
|:--|:--:|:--:|:--|
| FastAPI (direct) | `8000` | `8001` | http://localhost:8001 |
| Nginx (reverse proxy) | `80` | `8080` | http://localhost:8080 |
| Swagger UI | `8000` | `8001` | http://localhost:8001/docs |
| Health Check | `8000` | `8001` | http://localhost:8001/health |
| Predict API | `8000` | `8001` | http://localhost:8001/predict |
| All Classes | `8000` | `8001` | http://localhost:8001/classes |

---

## 14. Git Commands

```bash
# Clone
git clone https://github.com/Guna-kannan/PlantDiseaseDetector.git
cd PlantDiseaseDetector

# Check status
git status
git log --oneline -10

# Stage and commit
git add .
git commit -m "feat: your commit message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main

# View branches
git branch -a
```

**GitHub Repository:** https://github.com/Guna-kannan/PlantDiseaseDetector

---

## Quick Reference — All Commands at a Glance

```bash
# ── LOCAL DEV ──────────────────────────────────────────────────
uvicorn app:app --host 0.0.0.0 --port 8001 --reload    # Run server
python -m src.model data/PlantVillage                   # Train model
curl http://localhost:8001/health                        # Health check
curl -X POST -F "file=@leaf.jpg" http://localhost:8001/predict

# ── PODMAN ─────────────────────────────────────────────────────
podman build -f Containerfile -t plant-disease-detector:latest .
podman run -d -p 8001:8000 --name plant-disease-detector-app plant-disease-detector:latest
podman ps && podman logs -f plant-disease-detector-app
podman stop plant-disease-detector-app && podman rm plant-disease-detector-app

# ── COMPOSE ────────────────────────────────────────────────────
podman-compose up --build -d
podman-compose ps
podman-compose logs -f
podman-compose down

# ── KUBERNETES ─────────────────────────────────────────────────
kubectl apply -k k8s/
kubectl get pods -n plant-disease-detector
kubectl logs -l app=plant-disease-detector -n plant-disease-detector -f

# ── OPENSHIFT ──────────────────────────────────────────────────
oc apply -f openshift/
oc start-build plant-disease-detector --follow
oc get route plant-disease-detector -o jsonpath='{.spec.host}'

# ── GIT ────────────────────────────────────────────────────────
git add . && git commit -m "update" && git push origin main
```

---

*PlantDiseaseDetector · CNN Plant Leaf Disease Classifier · FastAPI + Podman + Kubernetes + OpenShift*
