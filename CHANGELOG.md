# Changelog

All notable changes to this project are documented in this file.

## [0.2.0] - 2026-07-24

### Added
- Input validation on `pg_connection_url` requiring `{{username}}` and `{{password}}` placeholders.
- Test coverage for the `rotate_root = true` code path.
- `allowed_roles` entry in the no-code form fields table.

## [0.1.1] - 2026-07-07

### Changed
- Documentation: renamed the "principal" layer references to "workload" to match the onboarding terminology (no input/output or behavior change).

## [0.1.0] - 2026-07-07

### Removed
- **Breaking:** removed the `vault_address` and `vault_namespace` input variables and their echo outputs. These inputs were echoed straight back as outputs and did no work in the module; downstream modules request these values as their own inputs.

## [0.0.2] - 2026-06-29

### Changed
- Documentation and version-consistency fixes: corrected the no-code registry pin, the registry-usage version constraint, and the CHANGELOG release header.

## [0.0.1]

### Added
- Initial no-code-ready module implementation.
