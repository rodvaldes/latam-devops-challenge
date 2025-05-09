#!/bin/bash

# Reemplaza con tu project ID y región
export PROJECT_ID=tu-proyecto-id
export REGION=us-central1

# Autenticación con Google
gcloud auth configure-docker

# Build de la imagen
docker build -t gcr.io/$PROJECT_ID/fastapi-app:latest .

# Push al Container Registry
docker push gcr.io/$PROJECT_ID/fastapi-app:latest
