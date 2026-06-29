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
| `pg_connection_url` | `string` | Connection URL with placeholders |
| `pg_username` | `string` | Root username, sensitive |
| `pg_password` | `string` | Root password, sensitive |
| `allowed_roles` | `string` | Optional allowed role glob |
| `rotate_root` | `bool` | Add root rotation statement, default `false` |
| `vault_namespace` | `string` | Render-only |
| `vault_address` | `string` | Render-only |

## Outputs

| Name | Description |
|---|---|
| `db_mount_path` | Database mount path |
| `db_connection_name` | Connection name |
| `cluster_name` | Echo |
| `vault_namespace` | Echo |
| `vault_address` | Echo |

## No-code notes

- This module is the shared database root configuration layer.
- It creates no principal, policy grant, identity group, or YAML snippets.

## Registry usage

```hcl
module "onboard_pgsql_connection" {
  source  = "app.terraform.io/<org>/onboard-pgsql-connection/vault"
  version = "~> 0.1"

  cluster_name      = "ocp-prod-eu"
  db_name           = "payments-db"
  pg_connection_url = "postgresql://{{username}}:{{password}}@db.example.com:5432/payments?sslmode=require"
  pg_username       = var.pg_username
  pg_password       = var.pg_password
}
```

Next step in chain: `terraform-vault-add-pgsql-role`.
