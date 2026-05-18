## Article MD1 — Local versus cloud execution is explicit

Plans say which work runs locally, which work runs in MotherDuck, and which data crosses that
boundary. This is required for cost, privacy, and reproducibility review.

## Article MD2 — Shares, databases, and collaborators are governed

Models and exports document MotherDuck database, share, role, and collaborator assumptions before
implementation.

## Article MD3 — File and object-store sources are reproducible

External files, object-store paths, and local development files are listed with CI or production
availability expectations.

## Article MD4 — Cost and quota impact is reviewed

Plans call out expected data volume, compute behavior, and any large scans or exports that may affect
MotherDuck quotas or spend.

## Article MD5 — Sensitive data is not casually synchronized

PII or restricted data crossing local/cloud boundaries requires masking, exclusion, or approved access
before implementation.
