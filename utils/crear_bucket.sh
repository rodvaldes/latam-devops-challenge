#!/bin/bash

PROJECT_ID=cyberstage
BUCKET_NAME=latam-data-terraform

gcloud config set project $PROJECT_ID

gcloud storage buckets create gs://$BUCKET_NAME \
  --location=us-central1 \
  --uniform-bucket-level-access
