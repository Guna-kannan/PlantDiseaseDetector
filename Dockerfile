FROM python:3.10-slim

LABEL maintainer="Guna Kannan" \
      version="1.0.0" \
      description="CNN-based Plant Disease Detector Container Image"

# System dependencies for TensorFlow + OpenCV + Healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Cache dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Application source
COPY . .

# Ensure storage directories exist and grant permissions
RUN mkdir -p models static/uploads && \
    chown -R 1001:0 /app && \
    chmod -R g+rwX /app

USER 1001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
