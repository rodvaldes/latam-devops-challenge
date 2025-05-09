resource "google_pubsub_topic" "this" {
  name = var.topic_name
  labels = var.labels
}

resource "google_pubsub_subscription" "this" {
  name  = var.subscription_name
  topic = google_pubsub_topic.this.id

  ack_deadline_seconds = var.ack_deadline_seconds
  retain_acked_messages = var.retain_acked_messages
  message_retention_duration = var.message_retention_duration

  labels = var.labels
}
