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
