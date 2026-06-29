mock_provider "vault" {}

run "invalid_db_name_fails_validation" {
  command = plan

  variables {
    cluster_name      = "dev-cluster"
    db_name           = "INVALID_NAME"
    pg_connection_url = "postgresql://{{username}}:{{password}}@db.example.com:5432/postgres?sslmode=disable"
    pg_password       = "root-password"
    pg_username       = "root"
  }

  expect_failures = [
    var.db_name,
  ]
}

run "invalid_cluster_name_fails_validation" {
  command = plan

  variables {
    cluster_name      = "-bad"
    db_name           = "appdb"
    pg_connection_url = "postgresql://{{username}}:{{password}}@db.example.com:5432/postgres?sslmode=disable"
    pg_password       = "root-password"
    pg_username       = "root"
  }

  expect_failures = [
    var.cluster_name,
  ]
}
