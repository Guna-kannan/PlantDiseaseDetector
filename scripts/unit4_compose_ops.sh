#!/bin/bash
# ==============================================================================
# Unit 4: Advanced Container Operations & Multi-Container Docker Compose
# ==============================================================================
# Demonstrates:
#  1. Multi-container orchestration: FastAPI backend + Nginx reverse proxy
#  2. Persistent data management (bind mounts for models and upload directory)
#  3. Container networking: custom bridge network and internal DNS resolution
#  4. Container debugging: logs inspection, health checks, and lifecycle commands
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

COMPOSE_TOOL="docker compose"
if ! docker compose version &> /dev/null; then
    if command -v podman-compose &> /dev/null; then
        COMPOSE_TOOL="podman-compose"
    fi
fi

echo -e "${BLUE}=== Unit 4: Advanced Container Operations & Compose ($COMPOSE_TOOL) ===${NC}\n"

echo -e "${GREEN}[1] Validating Compose Configuration:${NC}"
$COMPOSE_TOOL config
echo ""

echo -e "${GREEN}[2] Multi-Container Lifecycle Commands Reference:${NC}"
echo -e "${YELLOW}Start all services in detached mode:${NC}"
echo "  $COMPOSE_TOOL up --build -d"
echo ""
echo -e "${YELLOW}Inspect running container status and port mappings:${NC}"
echo "  $COMPOSE_TOOL ps"
echo ""
echo -e "${YELLOW}Follow logs across both services (FastAPI + Nginx):${NC}"
echo "  $COMPOSE_TOOL logs -f"
echo ""
echo -e "${YELLOW}Stop running services without removing containers:${NC}"
echo "  $COMPOSE_TOOL stop"
echo ""
echo -e "${YELLOW}Restart existing stopped containers:${NC}"
echo "  $COMPOSE_TOOL start"
echo ""
echo -e "${YELLOW}Teardown containers, networks, and internal resources:${NC}"
echo "  $COMPOSE_TOOL down"
echo ""
echo -e "${GREEN}[3] Storage & Networking Architecture:${NC}"
echo "  - Network: 'plant-net' (Bridge network providing DNS isolation)"
echo "  - Nginx Entrypoint: http://localhost:8080 (Reverse proxy with Gzip)"
echo "  - Backend Direct API: http://localhost:8001 (FastAPI inference engine)"
echo "  - Persistent Volumes: ./models (ro) and ./static/uploads (rw)"
echo ""

echo -e "${BLUE}=== Unit 4 Guide Completed ===${NC}"

