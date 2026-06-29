variable "allowed_roles" {
  type        = string
  description = "Role name glob allowed to register against this DB connection. Empty defaults to <cluster_name>-*."
  default     = ""
}

variable "cluster_name" {
  type        = string
  description = "Cluster identifier used in DB mount naming."

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{0,30}[a-z0-9]$", var.cluster_name))
    error_message = "cluster_name must match ^[a-z][a-z0-9-]{0,30}[a-z0-9]$."
  }
}

variable "db_name" {
  type        = string
  description = "Database logical identifier used in mount and connection naming."

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{0,30}[a-z0-9]$", var.db_name))
    error_message = "db_name must match ^[a-z][a-z0-9-]{0,30}[a-z0-9]$."
  }
}

variable "pg_connection_url" {
  type        = string
  description = "PostgreSQL connection URL with {{username}} and {{password}} placeholders."
  sensitive   = true
}

variable "pg_password" {
  type        = string
  description = "PostgreSQL root password used by the database secrets engine connection."
  sensitive   = true
}

variable "pg_username" {
  type        = string
  description = "PostgreSQL root username used by the database secrets engine connection."
  sensitive   = true
}

variable "rotate_root" {
  type        = bool
  description = "Whether to set root rotation statements on the connection."
  default     = false
}

variable "vault_address" {
  type        = string
  description = "Render-only Vault address value supplied via TF_VAR_vault_address."
  default     = ""
}

variable "vault_namespace" {
  type        = string
  description = "Render-only Vault namespace value supplied via TF_VAR_vault_namespace."
  default     = ""
}
