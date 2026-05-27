# Tata Consulting GitHub Activity Generation - Design Spec

**Date:** 2026-05-27
**Status:** Approved

## Overview

Generate a realistic, coherent story of engineering activity across the `tata-consulting` GitHub org using 13 authenticated accounts. Activity spans three overlapping phases over ~6 weeks, telling the story of an enterprise adopting cloud foundations, an Internal Developer Platform, and GitOps practices in parallel.

## Accounts

| Account | Role |
|---------|------|
| arjunmehta-git | Platform team lead |
| hamza-mohd | Cloud foundations engineer |
| sarajkrishnasingh | Platform engineer |
| winkletinkle | Platform/delivery engineer |
| miacycle | IDP contributor |
| pontusringblom | IDP contributor |
| ritzorama | Delivery/GitOps engineer |
| CodeAhmedJamil | GitOps engineer |
| yi-nuo426 | Integration engineer |
| hortison | SRE |
| alexquincy | Delivery engineer |
| jamieplu | Platform engineer |
| leecalcote | Architecture lead |

## Phases

### Phase 1 - Cloud Foundations (Apr 14 - May 4)

**Repos:** `tcs-cloud-foundations`, `crossplane`, `terraform-docs`
**Lead accounts:** `hamza-mohd`, `arjunmehta-git`, `sarajkrishnasingh`, `winkletinkle`

**Issues:**
- VPC module design and multi-region strategy
- IAM baseline policy framework
- Crossplane XRD design for AWS resources
- Add guardrail checklist for foundation changes (existing #2)
- Terraform module versioning strategy
- Cloud foundations onboarding guide

**PRs (mix of merged + open):**
- feat: AWS VPC Terraform module with multi-AZ support
- feat: IAM baseline roles and policies
- feat: Crossplane XRD for AWS RDS
- feat: Crossplane XRD for AWS S3
- docs: cloud foundations architecture overview
- chore: terraform-docs integration for module autodoc

**Commits to existing repos:**
- Terraform modules: `modules/vpc/`, `modules/iam/`, `modules/rds/`
- Crossplane compositions: `compositions/aws-rds.yaml`, `compositions/aws-s3.yaml`
- Meeting notes: `docs/meetings/2026-04-14-cloud-foundations-kickoff.md`
- Meeting notes: `docs/meetings/2026-04-28-guardrail-review.md`
- Architecture diagram (Mermaid): cloud foundation layers

### Phase 2 - IDP Build (Apr 28 - May 18)

**Repos:** `platform`, `tcs-platform-blueprints`, `backstage` fork
**Lead accounts:** `arjunmehta-git`, `sarajkrishnasingh`, `miacycle`, `pontusringblom`, `winkletinkle`

**Issues:**
- Backstage plugin inventory and selection
- Service catalog schema design
- Golden path template for Node.js services
- Golden path template for Python services
- TechDocs integration and publishing workflow
- Platform team RBAC model
- Blueprint maturity model definition
- Internal portal domain name and DNS

**PRs (mix of merged + open):**
- feat: Backstage app-config with TCS branding
- feat: software catalog - core entities
- feat: golden path template - Node.js microservice
- feat: golden path template - Python service
- feat: TechDocs MkDocs integration
- feat: platform blueprints - microservices pattern
- feat: platform blueprints - event-driven pattern
- docs: IDP architecture and onboarding guide

**Content:**
- Backstage YAML configs, software templates
- Meeting notes: `docs/meetings/2026-05-05-platform-team-standup.md`
- Meeting notes: `docs/meetings/2026-05-12-blueprint-review.md`
- Architecture diagram (Mermaid): IDP component architecture
- Architecture diagram (Mermaid): service catalog entity relationships

### Phase 3 - GitOps Adoption (May 12 - May 27)

**Repos:** `argo-cd` fork, `keda`, `tcs-delivery-accelerators`, `tcs-integration-starters`
**Accounts:** All 13

**Issues:**
- ArgoCD RBAC and project isolation design
- App-of-apps pattern vs ApplicationSet decision
- KEDA scaling policy for event-driven services
- KEDA HTTP add-on evaluation
- Delivery pipeline template for microservices
- Progressive delivery with Argo Rollouts
- Integration starter for Kafka
- Integration starter for RabbitMQ
- Integration starter for REST APIs
- Observability integration in delivery pipelines

**PRs (mix of merged + open):**
- feat: ArgoCD app-of-apps bootstrap
- feat: ArgoCD ApplicationSet for team namespaces
- feat: KEDA ScaledObject templates
- feat: delivery accelerator - CI pipeline starter
- feat: delivery accelerator - CD pipeline with ArgoCD
- feat: integration starter - Kafka producer/consumer
- feat: integration starter - REST API with OpenAPI
- docs: GitOps adoption guide

**Content:**
- ArgoCD Application manifests, ApplicationSet specs
- KEDA ScaledObject YAML templates
- Helm chart starters
- Meeting notes: `docs/meetings/2026-05-19-gitops-working-group.md`
- Meeting notes: `docs/meetings/2026-05-26-delivery-retrospective.md`
- Architecture diagram (Mermaid): GitOps delivery pipeline

## Volume Targets

| Type | Count |
|------|-------|
| Issues | ~40 |
| PRs | ~25 (mix merged/open) |
| Commits | ~60+ |
| Meeting notes | 6 |
| Architecture diagrams | 4 |
| Code files | ~30 |

## Execution Notes

- Switch `gh` account per action: `gh auth switch --user <account>`
- Use `--created-at` style backdating where GitHub API supports it; otherwise use commit date overrides via `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE`
- Issues and PR comments rotated across multiple accounts to simulate real team discussion
- PRs should have review comments from at least one other account before merge
- Meeting notes follow consistent template: attendees, agenda, decisions, action items
