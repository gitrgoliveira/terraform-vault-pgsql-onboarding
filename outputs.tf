output "cluster_name" {
  description = "Echo of cluster_name input."
  value       = var.cluster_name
}

output "db_connection_name" {
  description = "Database backend connection name used by downstream role module."
  value       = vault_database_secret_backend_connection.this.name
}

output "db_mount_path" {
  description = "Database backend mount path used by downstream role module."
  value       = vault_mount.this.path
}

output "vault_address" {
  description = "Echo of render-only vault_address."
  value       = var.vault_address
}

output "vault_namespace" {
  description = "Echo of render-only vault_namespace."
  value       = var.vault_namespace
}
