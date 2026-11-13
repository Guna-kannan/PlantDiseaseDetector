#!/bin/bash
# ==============================================================================
# Unit 2: Introduction to Containers & Podman Workflow
# ==============================================================================
# Demonstrates:
#  1. Podman features (Daemonless, Rootless, OCI compliant, Pod-native)
#  2. Installing & setting up Podman on RHEL: 'sudo dnf install -y podman'
#  3. Pulling base images
#  4. Building and running rootless containers
#  5. Creating and managing Podman Pods
#  6. Managing container lifecycle (start, stop, logs, inspect, rm)
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

CONTAINER_TOOL="podman"
if ! command -v podman &> /dev/null; then
    if command -v docker &> /dev/null; then
        echo -e "${YELLOW}Podman not found in PATH; falling back to Docker for demo.${NC}"
        CONTAINER_TOOL="docker"
    else
        echo "Error: Neither podman nor docker found."
        exit 1
    fi
fi

echo -e "${BLUE}=== Unit 2: Containers & Podman Workflow with $CONTAINER_TOOL ===${NC}\n"

# 1. Verification of Engine
echo -e "${GREEN}[1] Container Engine Info:${NC}"
$CONTAINER_TOOL version
echo ""

# 2. Pulling an OCI Image
echo -e "${GREEN}[2] Pulling an image from registry (python:3.10-slim):${NC}"
$CONTAINER_TOOL pull python:3.10-slim
echo ""

# 3. Building image using Containerfile
echo -e "${GREEN}[3] Building image using Containerfile:${NC}"
$CONTAINER_TOOL build -f Containerfile -t plant-disease-detector:local .
echo ""

# 4. Podman Pod Management (Pod-native architecture)
if [ "$CONTAINER_TOOL" == "podman" ]; then
    echo -e "${GREEN}[4] Creating a Podman Pod with shared network namespace:${NC}"
    podman pod create --name plant-pod -p 8001:8000 || true
    echo "Running container inside Podman Pod:"
    podman run -d --pod plant-pod \
        --name plant-detector-pod-app \
        -v "$(pwd)/models:/app/models:ro" \
        plant-disease-detector:local
    podman pod ps
    podman pod stop plant-pod
    podman pod rm -f plant-pod
else
    echo -e "${GREEN}[4] Running Container Lifecycle Demo:${NC}"
    $CONTAINER_TOOL run -d \
        --name plant-detector-test \
        -p 8001:8000 \
        -v "$(pwd)/models:/app/models:ro" \
        plant-disease-detector:local

    echo "Container status:"
    $CONTAINER_TOOL ps --filter "name=plant-detector-test"

    echo "Fetching container logs:"
    $CONTAINER_TOOL logs --tail 10 plant-detector-test

    echo "Stopping container:"
    $CONTAINER_TOOL stop plant-detector-test

    echo "Removing container:"
    $CONTAINER_TOOL rm plant-detector-test
fi

echo ""
echo -e "${BLUE}=== Unit 2 Demonstration Completed Successfully ===${NC}"

