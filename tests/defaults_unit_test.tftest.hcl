mock_provider "vault" {}

run "rotate_root_plan_succeeds" {
  command = plan

  variables {
    cluster_name      = "dev-cluster"
    db_name           = "appdb"
    pg_connection_url = "postgresql://{{username}}:{{password}}@db.example.com:5432/postgres?sslmode=disable"
    pg_password       = "root-password"
    pg_username       = "root"
    rotate_root       = true
  }

  assert {
    condition     = output.cluster_name == "dev-cluster"
    error_message = "cluster_name output should echo input."
  }

  assert {
    condition     = output.db_connection_name == "appdb"
    error_message = "db_connection_name output should match db_name."
  }

  assert {
    condition     = output.db_mount_path == "db/dev-cluster/appdb"
    error_message = "db_mount_path should be derived as db/<cluster_name>/<db_name>."
  }
}

run "defaults_plan_succeeds" {
  command = plan

  variables {
    cluster_name      = "dev-cluster"
    db_name           = "appdb"
    pg_connection_url = "postgresql://{{username}}:{{password}}@db.example.com:5432/postgres?sslmode=disable"
    pg_password       = "root-password"
    pg_username       = "root"
  }

  assert {
    condition     = output.cluster_name == "dev-cluster"
    error_message = "cluster_name output should echo input."
  }

  assert {
    condition     = output.db_connection_name == "appdb"
    error_message = "db_connection_name output should match db_name."
  }

  assert {
    condition     = output.db_mount_path == "db/dev-cluster/appdb"
    error_message = "db_mount_path should be derived as db/<cluster_name>/<db_name>."
  }
}
