provider "vault" {
  skip_child_token = true
}

locals {
  allowed_roles_effective = var.allowed_roles != "" ? var.allowed_roles : "${var.cluster_name}-*"
  db_mount_path           = "db/${var.cluster_name}/${var.db_name}"
}

resource "vault_mount" "this" {
  path = local.db_mount_path
  type = "database"
}

resource "vault_database_secret_backend_connection" "this" {
  backend       = vault_mount.this.path
  name          = var.db_name
  plugin_name   = "postgresql-database-plugin"
  allowed_roles = [local.allowed_roles_effective]

  postgresql {
    connection_url = var.pg_connection_url
    username       = var.pg_username
    password       = var.pg_password
  }

  root_rotation_statements = var.rotate_root ? ["ALTER USER {{username}} WITH PASSWORD '{{password}}';"] : null
}
