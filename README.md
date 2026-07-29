# terraform-vault-pgsql-onboarding

Use-case root-configuration module that mounts the database secrets engine and creates one PostgreSQL connection.

## Layer

Use-case root configuration.

## Prerequisites

- HCP Terraform project configured with Vault dynamic credentials
- PostgreSQL reachable from Vault

## Inputs

| Name | Type | Description |
|---|---|---|
| `cluster_name` | `string` | Cluster identifier, regex validated |
| `db_name` | `string` | Database identifier, regex validated |
| `pg_connection_url` | `string` | Connection URL with placeholders, sensitive |
| `pg_username` | `string` | Root username, sensitive |
| `pg_password` | `string` | Root password, sensitive |
| `allowed_roles` | `string` | Optional allowed role glob |
| `rotate_root` | `bool` | Add root rotation statement, default `false` |

## Outputs

| Name | Description |
|---|---|
| `db_mount_path` | Database mount path |
| `db_connection_name` | Connection name |
| `cluster_name` | Echo |

## No-code notes

- This module is the shared database root configuration layer.
- It creates no workload, policy grant, identity group, or YAML snippets.

## No-code provisioning

This module is no-code enabled in the `hc-ric-demo` private registry (pinned to `0.2.0`). Click **Provision workspace**, pick a project and workspace name, then complete the form. `pg_connection_url`, `pg_username`, and `pg_password` are sensitive.

Form fields:

| Field | Required | Notes |
|---|---|---|
| `cluster_name` | yes | Cluster identifier |
| `db_name` | yes | Database identifier |
| `pg_connection_url` | yes | Root DB connection URL with `{{username}}`/`{{password}}` placeholders (sensitive) |
| `pg_username` | yes | Root username (sensitive) |
| `pg_password` | yes | Root password (sensitive) |
| `allowed_roles` | no | Glob pattern for allowed role names (defaults to `<cluster_name>-*` when empty) |
| `rotate_root` | no | Default `false` |

## Registry usage

```hcl
module "onboard_pgsql_connection" {
  source  = "app.terraform.io/<org>/onboard-pgsql-connection/vault"
  version = "~> 0.2.0"

  cluster_name      = "ocp-prod-eu"
  db_name           = "payments-db"
  # Sensitive — supply via a sensitive workspace variable, never a literal in HCL.
  # Format: postgresql://{{username}}:{{password}}@<host>:5432/<db>?sslmode=require
  pg_connection_url = var.pg_connection_url
  pg_username       = var.pg_username
  pg_password       = var.pg_password
}
```

Next step in chain: `terraform-vault-add-pgsql-role`.
