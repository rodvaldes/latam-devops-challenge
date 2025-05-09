output "topic_id" {
  value = google_pubsub_topic.this.id
}

output "subscription_id" {
  value = google_pubsub_subscription.this.id
}
