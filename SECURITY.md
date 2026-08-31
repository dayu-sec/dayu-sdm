# Security Policy

This repository publishes a **data model standard** (schema, contracts, field catalogs, and sanitized examples). It is not a network service.

## Reporting a vulnerability

If you find credentials, customer identifiers, real IP addresses, or other sensitive data in examples or docs, please **do not** open a public issue.

Contact **dayu-sec** maintainers via the GitHub repository, or open a private security advisory.

## Scope

In scope:

- Secrets or PII that slipped into examples, docs, or presentation pages
- Unsafe defaults in published DDL / Routine Load templates that would expose a deployment if copied verbatim

Out of scope:

- Vendor product vulnerabilities mentioned in sample logs
- Mapping completeness of third-party log formats
