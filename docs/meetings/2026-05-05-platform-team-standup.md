# Platform Team Standup - Sprint Review
**Date:** 2026-05-05
**Attendees:** Arjun Mehta, Saraj Krishna Singh, Mia Cycle, Pontus Ringblom, Winkletinkle
**Sprint:** Platform IDP - Sprint 2

## Status Updates

**Saraj (Node.js golden path template):**
First draft of scaffolder template complete. Generates: Express app skeleton, Dockerfile (multi-stage, alpine), GitHub Actions CI workflow, catalog-info.yaml with mandatory annotations, basic Helm chart. Needs review on Helm chart resource limits.

**Pontus (Python golden path template):**
In progress. FastAPI skeleton done, Dockerfile done. CI workflow and MkDocs setup remaining. ETA: end of week.

**Mia (TechDocs pipeline):**
S3 bucket provisioned in dev. Reusable GitHub Actions workflow drafted. Testing with the platform repo's own TechDocs - finding some issues with MkDocs plugin version compatibility.

**Winkletinkle (Service catalog population):**
Started populating catalog with first 5 internal services. Hitting annotation inconsistency - teams have slightly different formats. Proposing a catalog linting step in CI.

**Arjun (Backstage app-config):**
App-config for dev environment is deployed. GitHub OAuth working. EKS plugin configured and showing cluster data. Proceeding to production app-config.

## Blockers
- MkDocs plugin version compatibility (Mia) - investigating, ETA tomorrow
- Service catalog annotation inconsistency (Winkletinkle) - proposing lint step PR

## Action Items
| Owner | Action | Due |
|-------|--------|-----|
| Saraj | Request review on Node.js template PR | 2026-05-06 |
| Pontus | Complete Python template | 2026-05-09 |
| Mia | Resolve MkDocs version issue | 2026-05-06 |
| Winkletinkle | PR for catalog-info linting CI step | 2026-05-07 |
| Arjun | Draft production app-config | 2026-05-08 |
