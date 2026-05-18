# Azure SQL guide

Use this preset when dbt targets Azure SQL Database or Azure SQL Managed Instance.

## What the preset adds

- service tier, elastic pool, CPU, IO, and log-pressure planning
- Query Store evidence expectations for performance-sensitive work
- index, columnstore, and incremental load guardrails
- Microsoft Entra, role, RLS, dynamic masking, and view-boundary review
- firewall, private endpoint, and deployment-window callouts

## Good fit

- Azure-native enterprise teams
- shared elastic pool environments
- governed marts using Azure SQL serving layers

## Use

```bash
dbt-specify init analytics --warehouse azure-sql
```

This is a planning preset. It does not configure Azure credentials, networking, or dbt profiles.
