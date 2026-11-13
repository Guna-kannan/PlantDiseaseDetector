#!/bin/bash
# ==============================================================================
# Unit 3: Building and Managing Container Images & Registry Workflow
# ==============================================================================
# Demonstrates:
#  1. Container image layer inspection
#  2. Efficient & secure build best practices (slim base, multi-stage, non-root)
#  3. Tagging images with versioning and registry namespaces (Quay.io / Docker Hub)
#  4. Pushing and pulling images from remote container registries
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

REGISTRY="quay.io"
NAMESPACE="${REGISTRY_NAMESPACE:-gunakannan}"
IMAGE_NAME="plant-disease-detector"
VERSION="v1.0.0"

CONTAINER_TOOL="podman"
if ! command -v podman &> /dev/null; then
    CONTAINER_TOOL="docker"
fi

echo -e "${BLUE}=== Unit 3: Container Image Build & Registry Workflow ($CONTAINER_TOOL) ===${NC}\n"

# 1. Building the Image with metadata tags
echo -e "${GREEN}[1] Building container image from Containerfile/Dockerfile:${NC}"
$CONTAINER_TOOL build -f Containerfile -t "${IMAGE_NAME}:${VERSION}" .
echo ""

# 2. Inspecting Image Layers & Size
echo -e "${GREEN}[2] Inspecting Image History and Layer Cache:${NC}"
$CONTAINER_TOOL history "${IMAGE_NAME}:${VERSION}"
echo ""

# 3. Tagging for Remote Registries (Quay.io / Docker Hub)
echo -e "${GREEN}[3] Tagging Image for Remote Registry (${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}):${NC}"
$CONTAINER_TOOL tag "${IMAGE_NAME}:${VERSION}" "${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
$CONTAINER_TOOL tag "${IMAGE_NAME}:${VERSION}" "${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:latest"
echo "Tagged images:"
$CONTAINER_TOOL images | grep "${IMAGE_NAME}"
echo ""

# 4. Registry Push Guide
echo -e "${GREEN}[4] Registry Push & Pull Commands:${NC}"
echo -e "${YELLOW}To log in and push to registry, execute:${NC}"
echo "  1. $CONTAINER_TOOL login $REGISTRY"
echo "  2. $CONTAINER_TOOL push ${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
echo "  3. $CONTAINER_TOOL push ${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:latest"
echo ""
echo -e "${YELLOW}To pull and run on another host:${NC}"
echo "  1. $CONTAINER_TOOL pull ${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
echo "  2. $CONTAINER_TOOL run -d -p 8000:8000 ${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
echo ""

echo -e "${BLUE}=== Unit 3 Demonstration Completed Successfully ===${NC}"

