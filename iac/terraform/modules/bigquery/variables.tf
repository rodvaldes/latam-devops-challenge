variable "project_id" {
  type        = string
  description = "ID del proyecto GCP"
}

variable "region" {
  type        = string
  description = "Región donde se creará el dataset"
}

variable "dataset_id" {
  type        = string
  description = "ID del dataset"
}

variable "friendly_name" {
  type        = string
  default     = null
  description = "Nombre amigable del dataset"
}

variable "description" {
  type        = string
  default     = null
  description = "Descripción del dataset"
}

variable "delete_contents_on_destroy" {
  type        = bool
  default     = false
}

variable "labels" {
  type        = map(string)
  default     = {}
  description = "Etiquetas del dataset"
}

variable "tables" {
  type = map(object({
    schema = string
  }))
  default     = {}
  description = "Map de tablas con sus esquemas JSON"
}
