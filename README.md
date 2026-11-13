# PlantDiseaseDetector

PlantDiseaseDetector is an end-to-end CNN-based plant disease classifier for leaf images with full cloud-native DevOps containerization and orchestration support. It predicts the disease class, confidence score, severity level, treatment recommendation, and top three candidate classes for Tomato, Potato, and Bell Pepper leaves.

The model is trained on the PlantVillage dataset with 15 supported classes.

---

## Supported Classes

| Class name | Crop | Severity |
| --- | --- | --- |
| `Pepper__bell___Bacterial_spot` | Bell Pepper | Moderate |
| `Pepper__bell___healthy` | Bell Pepper | None |
| `Potato___Early_blight` | Potato | Moderate |
| `Potato___Late_blight` | Potato | High |
| `Potato___healthy` | Potato | None |
| `Tomato_Bacterial_spot` | Tomato | Moderate |
| `Tomato_Early_blight` | Tomato | Moderate |
| `Tomato_Late_blight` | Tomato | High |
| `Tomato_Leaf_Mold` | Tomato | Moderate |
| `Tomato_Septoria_leaf_spot` | Tomato | Moderate |
| `Tomato_Spider_mites_Two_spotted_spider_mite` | Tomato | Moderate |
| `Tomato__Target_Spot` | Tomato | Moderate |
| `Tomato__Tomato_YellowLeaf__Curl_Virus` | Tomato | High |
| `Tomato__Tomato_mosaic_virus` | Tomato | High |
| `Tomato_healthy` | Tomato | None |

---

## Tech Stack & DevOps Ecosystem

- **Machine Learning & Backend:** Python 3.10, TensorFlow/Keras 2.15, NumPy, Pillow, FastAPI, Uvicorn, Jinja2
- **Linux & OS Administration:** Red Hat Enterprise Linux (RHEL) / Debian, Bash scripting, system utilities (`grep`, `tar`, `gzip`, `bzip2`)
- **Container Engines:** Podman (Rootless, Daemonless, Pod-native) & Docker Engine
- **Image Specifications:** OCI Standard `Containerfile` and `Dockerfile`
- **Orchestration & Multi-Container:** Docker Compose / Podman Compose, Nginx Reverse Proxy
- **Cloud Orchestration:** Kubernetes (Deployments, Services, PVCs, Ingress) & Red Hat OpenShift (BuildConfigs, ImageStreams, Routes)
- **Container Registries:** Quay.io / Docker Hub / OpenShift Internal Registry

---

## Project Structure

```text
PlantDiseaseDetector/
├── app.py                            # FastAPI application entrypoint
├── Containerfile                     # OCI & Podman/RHEL compliant container image spec
├── Dockerfile                        # Docker image specification
├── docker-compose.yml                # Multi-container orchestration (FastAPI + Nginx)
├── requirements.txt                  # Python runtime dependencies
├── README.md                         # Comprehensive documentation & curriculum guide
├── nginx/
│   └── nginx.conf                    # Reverse proxy & gzip configuration
├── k8s/                              # Kubernetes manifests
│   ├── namespace.yaml                # Dedicated namespace
│   ├── pvc.yaml                      # Persistent storage for models & uploads
│   ├── deployment.yaml               # Multi-pod deployment (2 replicas, health probes)
│   ├── service.yaml                  # ClusterIP service
│   ├── ingress.yaml                  # Ingress routing
│   └── kustomization.yaml            # Single-command deployment bundle
├── openshift/                        # Red Hat OpenShift manifests
│   ├── imagestream.yaml              # OpenShift ImageStream
│   ├── buildconfig.yaml              # OpenShift in-cluster Git build config
│   ├── deployment.yaml               # OpenShift SCC-compliant deployment
│   ├── service.yaml                  # Service definition
│   └── route.yaml                    # OpenShift edge-terminated Route
├── scripts/                          # Demonstration & verification scripts
│   ├── unit1_linux_basics.sh         # Linux administration & tool verification
│   ├── unit2_podman_workflow.sh      # Podman lifecycle & Pod management
│   ├── unit3_registry_workflow.sh    # Image building, tagging & registry push
│   ├── unit4_compose_ops.sh          # Multi-container Compose operations
│   └── unit5_k8s_openshift.sh        # Kubernetes & OpenShift operations
├── models/
│   ├── plant_disease_model.keras     # Trained CNN model
│   └── training_history.png          # Training and validation loss/accuracy curves
├── src/
│   ├── __init__.py
│   ├── model.py                      # CNN architecture, training & evaluation
│   └── predictor.py                  # Inference logic & metadata enrichment
├── static/
│   └── uploads/                      # Uploaded leaf images for prediction
└── templates/
    └── index.html                    # Web upload & classification UI
```

---

## Syllabus & Curriculum Implementation Guide

This project includes implementations and practical workflows for all five DevOps and containerization units:

### Unit 1 – Basics of Linux & Essential Administration

Covers Linux system management, text processing, archiving, permissions, and storage:

1. **System & Kernel Details:**
   ```bash
   uname -a
   cat /etc/os-release
   ```
2. **Text Processing & Searching (`grep`):**
   ```bash
   grep -rn "CLASS_NAMES" src/
   ```
3. **Archiving & Compression (`tar`, `gzip`, `bzip2`):**
   ```bash
   tar -cvf backup.tar models/
   gzip -k backup.tar       # creates backup.tar.gz
   bzip2 -k backup.tar      # creates backup.tar.bz2
   ```
4. **File Permissions (`chmod`, `chown`):**
   ```bash
   chmod u=rw,go=r models/plant_disease_model.keras   # 644
   chmod -R g+rwX /app                                # Group inheritance for non-root containers
   ```
5. **Local Storage & Partitions (MBR vs GPT):**
   - **MBR:** Legacy BIOS, max 4 primary partitions, 2 TB disk limit.
   - **GPT:** Modern UEFI, up to 128 partitions, 9.4 ZB capacity, CRC32 data integrity.
   - Inspect mounted storage: `df -h` or `lsblk` / `fdisk -l`.
6. **User & Group Administration:**
   ```bash
   id
   groups
   sudo useradd -m -s /bin/bash appuser
   sudo usermod -aG appgroup appuser
   ```
7. **Run Unit 1 automated demo script:**
   ```bash
   ./scripts/unit1_linux_basics.sh
   ```

---

### Unit 2 – Introduction to Containers and Podman

Demonstrates rootless, daemonless container management and pod-native architecture:

1. **Install Podman on RHEL:**
   ```bash
   sudo dnf install -y podman
   ```
2. **Inspect Engine Information:**
   ```bash
   podman version
   podman info
   ```
3. **Pull Base Image:**
   ```bash
   podman pull python:3.10-slim
   ```
4. **Build Image using `Containerfile`:**
   ```bash
   podman build -f Containerfile -t plant-disease-detector:local .
   ```
5. **Podman Pod Creation (Native multi-container pod):**
   ```bash
   # Create a shared network pod
   podman pod create --name plant-pod -p 8001:8000

   # Run container inside the pod
   podman run -d --pod plant-pod --name plant-detector-app plant-disease-detector:local

   # Inspect and manage pod
   podman pod ps
   podman pod stop plant-pod
   podman pod rm -f plant-pod
   ```
6. **Run Unit 2 automated script:**
   ```bash
   ./scripts/unit2_podman_workflow.sh
   ```

---

### Unit 3 – Building and Managing Container Images

Demonstrates container image structure, optimization, security, and registry workflows:

1. **Best Practices Implemented in `Containerfile` & `Dockerfile`:**
   - **Minimal Base Image:** Uses `python:3.10-slim` to reduce attack surface and download size.
   - **Layer Caching:** Copies `requirements.txt` before code to avoid re-installing packages when code changes.
   - **Non-Root User:** Runs as non-root user (`USER 1001`) with group permissions for security compliance.
   - **Healthcheck:** Embedded `HEALTHCHECK` probe verifying HTTP endpoint `/health`.
2. **Image Inspection:**
   ```bash
   podman history plant-disease-detector:local
   ```
3. **Tagging for Container Registries (Quay.io / Docker Hub):**
   ```bash
   podman tag plant-disease-detector:local quay.io/<username>/plant-disease-detector:v1.0.0
   podman tag plant-disease-detector:local quay.io/<username>/plant-disease-detector:latest
   ```
4. **Pushing to Registry:**
   ```bash
   podman login quay.io
   podman push quay.io/<username>/plant-disease-detector:v1.0.0
   podman push quay.io/<username>/plant-disease-detector:latest
   ```
5. **Run Unit 3 automated script:**
   ```bash
   ./scripts/unit3_registry_workflow.sh
   ```

---

### Unit 4 – Advanced Container Usage (Volumes, Networks & Compose)

Demonstrates multi-container architecture, persistent storage, and service communication:

1. **Architecture:**
   - **Frontend/Reverse Proxy:** Nginx (`nginx:alpine`) on port `8080`, providing reverse proxying, client header forwarding, and Gzip compression.
   - **Backend Application:** FastAPI (`plant-disease-detector`) on port `8000` (also reachable directly on `8001` for debugging).
   - **Private Network:** `plant-net` bridge network providing internal DNS service discovery.
   - **Persistent Storage:** Bind mounts for `./models` (read-only) and `./static/uploads` (read-write).
2. **Docker Compose Lifecycle Commands:**
   ```bash
   # Build and start all services in background
   docker compose up --build -d

   # Check status and port mappings
   docker compose ps

   # View real-time logs across services
   docker compose logs -f

   # Stop services without deleting containers
   docker compose stop

   # Restart stopped services
   docker compose start

   # Teardown containers, networks, and volumes
   docker compose down
   ```
3. **Access Services:**
   - Web App via Nginx Reverse Proxy: [http://localhost:8080](http://localhost:8080)
   - Direct Backend API: [http://localhost:8001](http://localhost:8001)
4. **Run Unit 4 verification script:**
   ```bash
   ./scripts/unit4_compose_ops.sh
   ```

---

### Unit 5 – Kubernetes & Red Hat OpenShift Orchestration

Demonstrates enterprise container orchestration, multi-pod scaling, health probes, and edge routing:

#### 1. Kubernetes Deployment
Deploy onto any Kubernetes cluster (Minikube, Kind, EKS, GKE):

```bash
# Deploy all resources (Namespace, PVC, Multi-Pod Deployment, Service, Ingress)
kubectl apply -k k8s/

# Verify multi-pod deployment (2 replicas)
kubectl get pods -n plant-disease-detector -o wide

# Check Service and PVC status
kubectl get svc,pvc,ingress -n plant-disease-detector

# Check rollout status
kubectl rollout status deployment/plant-disease-detector -n plant-disease-detector
```

#### 2. Red Hat OpenShift Deployment
Deploy onto Red Hat OpenShift Container Platform (or OpenShift Local / CRC):

```bash
# Log in to OpenShift
oc login -u <username> -p <password> https://api.crc.testing:6443

# Create or switch to project
oc new-project plant-disease-detector

# Create ImageStream and BuildConfig for automated builds
oc apply -f openshift/imagestream.yaml
oc apply -f openshift/buildconfig.yaml

# Trigger in-cluster image build
oc start-build plant-disease-detector --follow

# Deploy application and create Service
oc apply -f openshift/deployment.yaml
oc apply -f openshift/service.yaml

# Expose service with an edge-terminated OpenShift Route
oc apply -f openshift/route.yaml

# Retrieve public Route URL
oc get route plant-disease-detector -o jsonpath='{.spec.host}'
```

#### 3. Kubernetes & OpenShift Troubleshooting Commands:
```bash
# Inspect Pod events and diagnostic messages (ImagePullBackOff, CrashLoopBackOff, etc.)
kubectl describe pod <pod-name> -n plant-disease-detector
oc describe pod <pod-name>

# View multi-pod application logs
kubectl logs -l app=plant-disease-detector -n plant-disease-detector --all-containers=true -f

# Check cluster event stream
kubectl get events -n plant-disease-detector --sort-by='.metadata.creationTimestamp'

# Open an interactive shell inside a running container
kubectl exec -it <pod-name> -n plant-disease-detector -- /bin/sh
```
4. **Run Unit 5 reference script:**
   ```bash
   ./scripts/unit5_k8s_openshift.sh
   ```

---

## Local Development & Python Setup

1. **Virtual Environment:**
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Train Model (Optional if model already trained):**
   ```bash
   python -m src.model data/PlantVillage
   ```

3. **Run Web App Locally:**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8001 --reload
   ```
   Open: [http://localhost:8001](http://localhost:8001)

---

## REST API Specification

| Route | Method | Description |
| --- | --- | --- |
| `/` | GET | Web browser user interface |
| `/predict` | POST | Accepts multipart image upload, returns JSON classification |
| `/health` | GET | Healthcheck endpoint (`status: ok`, `model_loaded: true`) |
| `/classes` | GET | List of all 15 supported disease classes |
| `/docs` | GET | Interactive Swagger API documentation |

---

## Model Evaluation Results

| Metric | Value |
| --- | --- |
| **Model Architecture** | 6-Block CNN + Dropout(0.4) + Dense(15, Softmax) |
| **Input Shape** | 256 × 256 × 3 |
| **Batch Size** | 32 |
| **Data Split** | 80% Train, 10% Validation, 10% Test |
| **Early Stopping** | Patience = 5 epochs on validation loss |
| **Training Curves** | Saved to [`models/training_history.png`](models/training_history.png) |

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
