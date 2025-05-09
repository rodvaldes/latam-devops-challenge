terraform {
  required_version = ">= 1.3.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket = "latam-data-terraform"
    prefix = "state"
  }
}

module "bigquery_core" {
  source     = "./modules/bigquery"       # Ruta al módulo
  dataset_id = "challenge"                # ID del dataset en BigQuery
  project_id = var.project_id             # Proyecto GCP (desde variables.tf)
  region     = var.region                 # Región donde se crea el dataset

  friendly_name = "Core Analytics Dataset" # Nombre visible en BigQuery
  description   = "Datos centrales de la aerolínea"
  delete_contents_on_destroy = false       # No elimina las tablas si se destruye el recurso

  labels = {
    environment = var.environment         # Etiquetas útiles para organización
    team        = "analytics"
  }

  tables = {
    # Definición de tablas en el dataset
    raw_events = {
    schema = file("${path.module}/schemas/raw_events_schema.json")

    }
  }
}

module "pubsub_flight_events" {
  source = "./modules/pubsub"

  topic_name        = "flight-events"
  subscription_name = "flight-events-sub"

  labels = {
    environment = var.environment
    team        = "analytics"
  }

  ack_deadline_seconds       = 20
  retain_acked_messages      = true
  message_retention_duration = "86400s" # 1 día
}

