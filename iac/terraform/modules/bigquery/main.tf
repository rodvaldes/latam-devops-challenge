resource "google_bigquery_dataset" "this" {
  dataset_id                  = var.dataset_id
  project                     = var.project_id
  location                    = var.region
  friendly_name               = var.friendly_name
  description                 = var.description
  delete_contents_on_destroy = var.delete_contents_on_destroy
  labels                      = var.labels
}

resource "google_bigquery_table" "tables" {
  for_each = var.tables

  dataset_id = google_bigquery_dataset.this.dataset_id
  table_id   = each.key
  schema     = each.value.schema
  project    = var.project_id
  deletion_protection = false
}
