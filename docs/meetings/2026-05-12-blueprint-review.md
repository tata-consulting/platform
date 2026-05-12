# Platform Blueprint Review
**Date:** 2026-05-12
**Attendees:** Arjun Mehta, Saraj Krishna Singh, Mia Cycle, Pontus Ringblom, Winkletinkle
**Type:** Blueprint design review

## Agenda
1. Node.js golden path - review and sign-off
2. Python golden path - review and sign-off
3. Microservices blueprint - review patterns and standards
4. Blueprint maturity model

## Discussion

### Node.js Golden Path
Reviewed. Approved with minor changes:
- Add `tier` input defaulting to `tier-2`
- Add checkov scan step to CI workflow
- Helm chart: add HPA and proper resource requests/limits
Saraj to apply changes, then merge.

### Python Golden Path
Reviewed. Approved with same changes as Node.js plus:
- Switch base image from `python:3.12-slim` to `python:3.12-alpine` for smaller images
- Add `ruff` configuration in `pyproject.toml`
Pontus to apply, then merge.

### Microservices Blueprint
Draft reviewed. Key decisions:
- mTLS: "service mesh optional, mTLS via cert-manager if no mesh" (not prescriptive on Istio)
- Observability: OpenTelemetry SDK standard, export target is client-specific
- gRPC: deferred to v2 blueprint
Arjun to finalize and merge.

### Blueprint Maturity Model
Approved. Maturity annotation (`tcs.io/maturity`) and sunset date (`tcs.io/sunset-date` for deprecated) added to standards. Both golden paths will launch as `beta`.

## Decisions
1. Node.js and Python golden paths approved (with noted changes), launch as Beta
2. Microservices blueprint: mTLS pattern updated, launch as Beta
3. Blueprint maturity model: adopted

## Action Items
| Owner | Action | Due |
|-------|--------|-----|
| Saraj | Apply Node.js template feedback, merge | 2026-05-13 |
| Pontus | Apply Python template feedback, merge | 2026-05-14 |
| Arjun | Finalize microservices blueprint | 2026-05-15 |
| Mia | Add maturity annotations to all merged blueprints | 2026-05-15 |
