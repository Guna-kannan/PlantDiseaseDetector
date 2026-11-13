#!/bin/bash
# ==============================================================================
# Unit 5: Kubernetes & Red Hat OpenShift Deployment and Troubleshooting
# ==============================================================================
# Demonstrates:
#  1. Deploying multi-pod applications onto Kubernetes
#  2. Deploying containerized workloads onto Red Hat OpenShift
#  3. OpenShift Route creation and edge TLS termination
#  4. Managing resources and checking rollout status
#  5. Troubleshooting: pod status, events, logs, and resource limits
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=== Unit 5: Kubernetes & OpenShift Deployment Guide ===${NC}\n"

# Section A: Kubernetes Deployment Workflow
echo -e "${GREEN}[A] Kubernetes Deployment Commands:${NC}"
cat << 'EOF'
1. Create Namespace:
   kubectl apply -f k8s/namespace.yaml

2. Create Persistent Volume Claims:
   kubectl apply -f k8s/pvc.yaml

3. Deploy Multi-Pod Workload (2 Replicas with Health Probes):
   kubectl apply -f k8s/deployment.yaml

4. Expose Service and Ingress:
   kubectl apply -f k8s/service.yaml
   kubectl apply -f k8s/ingress.yaml

(Or deploy all at once using Kustomize):
   kubectl apply -k k8s/

5. Check Deployment & Multi-Pod Status:
   kubectl get pods -n plant-disease-detector -o wide
   kubectl get svc,pvc,ingress -n plant-disease-detector

6. Verify Rolling Update & Rollout:
   kubectl rollout status deployment/plant-disease-detector -n plant-disease-detector
EOF
echo ""

# Section B: Red Hat OpenShift Deployment Workflow
echo -e "${GREEN}[B] Red Hat OpenShift Deployment Commands:${NC}"
cat << 'EOF'
1. Log in to OpenShift Cluster:
   oc login -u <username> -p <password> https://api.crc.testing:6443

2. Create Project:
   oc new-project plant-disease-detector

3. Create ImageStream & BuildConfig (Source-to-Image / Docker build):
   oc apply -f openshift/imagestream.yaml
   oc apply -f openshift/buildconfig.yaml

4. Trigger OpenShift In-Cluster Build:
   oc start-build plant-disease-detector --follow

5. Deploy Application & Expose via OpenShift Route:
   oc apply -f openshift/deployment.yaml
   oc apply -f openshift/service.yaml
   oc apply -f openshift/route.yaml

6. Retrieve Public Route URL:
   oc get route plant-disease-detector -o jsonpath='{.spec.host}'
EOF
echo ""

# Section C: Troubleshooting Guide
echo -e "${GREEN}[C] Troubleshooting & Diagnostics (Best Practices):${NC}"
cat << 'EOF'
1. Check Pod details & event log (for ImagePullBackOff, CrashLoopBackOff, OOMKilled):
   kubectl describe pod <pod-name> -n plant-disease-detector
   oc describe pod <pod-name>

2. Stream logs from multi-pod replicas:
   kubectl logs -l app=plant-disease-detector -n plant-disease-detector --all-containers=true -f

3. Inspect OpenShift Cluster Status & Health:
   oc status
   oc get events --sort-by='.metadata.creationTimestamp'

4. Execute inside a live pod container for debugging:
   kubectl exec -it <pod-name> -n plant-disease-detector -- /bin/sh
EOF
echo ""

echo -e "${BLUE}=== Unit 5 Guide Completed ===${NC}"

