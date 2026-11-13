# Containerfile for Podman and Red Hat Enterprise Linux (RHEL) / OCI compliance
# Compatible with both Docker and Podman

FROM python:3.10-slim

# Labels adhering to OCI Image Format Specification
LABEL maintainer="Guna Kannan" \
      version="1.0.0" \
      description="CNN-based Plant Disease Detector Container Image" \
      io.k8s.description="FastAPI service for leaf disease classification" \
      io.k8s.display-name="Plant Disease Detector" \
      io.openshift.expose-services="8000:http" \
      io.openshift.tags="python,fastapi,tensorflow,machine-learning,plant-disease"

# Install minimal OS dependencies for TensorFlow and OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set standard working directory
WORKDIR /app

# Copy dependency definition first for optimal layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Ensure storage directories exist and grant permissions for OpenShift arbitrary non-root user (UID 1001 / root group GID 0)
RUN mkdir -p models static/uploads && \
    chown -R 1001:0 /app && \
    chmod -R g+rwX /app

# Non-root user for security best practices (Podman & OpenShift compliant)
USER 1001

# Expose standard application port
EXPOSE 8000

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start FastAPI inference server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

