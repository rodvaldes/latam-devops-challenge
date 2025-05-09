variable "topic_name" {
  type        = string
  description = "Nombre del tópico Pub/Sub"
}

variable "subscription_name" {
  type        = string
  description = "Nombre de la suscripción al tópico"
}

variable "ack_deadline_seconds" {
  type        = number
  default     = 10
  description = "Tiempo para hacer ACK del mensaje"
}

variable "retain_acked_messages" {
  type        = bool
  default     = false
  description = "Mantener mensajes ya confirmados"
}

variable "message_retention_duration" {
  type        = string
  default     = "604800s" # 7 días
  description = "Duración de retención del mensaje"
}

variable "labels" {
  type        = map(string)
  default     = {}
}
