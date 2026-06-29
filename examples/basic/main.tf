terraform {
  required_version = ">= 1.9"
}

module "onboard_pgsql_connection" {
  source = "../../"

  cluster_name      = var.cluster_name
  db_name           = var.db_name
  pg_connection_url = var.pg_connection_url
  pg_password       = var.pg_password
  pg_username       = var.pg_username
  rotate_root       = var.rotate_root
}

variable "cluster_name" {
  type        = string
  description = "Cluster identifier."
}

variable "db_name" {
  type        = string
  description = "Database identifier."
}

variable "pg_connection_url" {
  type        = string
  description = "PostgreSQL connection URL with placeholders."
  sensitive   = true
}

variable "pg_password" {
  type        = string
  description = "Root password."
  sensitive   = true
}

variable "pg_username" {
  type        = string
  description = "Root username."
  sensitive   = true
}

variable "rotate_root" {
  type        = bool
  description = "Whether to define root rotation statements."
  default     = false
}
